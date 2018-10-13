import properties
from properties import COVERAGE_THRESHOLD, MIN_ACCEPTABLE_COVERAGE
import utils
from utils import getMapCoverage
import math
from batteryEnum import LOW, CRITICAL, NORMAL
from altitudeEnum import TOO_LOW, TOO_HIGH, ALTITUDE_OK
import threading
from pyparrot.Bebop import Bebop
import random
import time
from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM, SH_NO_GREEDY
from algoritmo_aster import Pathfinder


class drone:
    def __init__(self, home):
        self.rango_largo = properties.RANGO_LARGO
        self.rango_ancho = properties.RANGO_ANCHO
        self.mapa_largo = properties.MAPA_LARGO / self.rango_largo
        self.mapa_ancho = properties.MAPA_ANCHO / self.rango_ancho
        self.ip = None
        self.port = None
        self.search_map = [[0 for j in range(int(self.mapa_largo))]for i in range(int(self.mapa_ancho))]
        self.current_position = home
        self.current_rotation = math.pi / 2
        self.mutex_search_map = threading.Lock()
        self.poi_position = None
        self.home = home
        self.bebop = Bebop()
        self.init_time = None
        self.obstaculos = properties.OBSTACLES
        self.max_altitude = properties.MAX_ALTITUDE
        self.pathToFollow = None
        self.destinationZone = None
        self.countIter = 0

    def initialize(self, ip, port):
        self.initSearchMapWithObstacles()
        if properties.ALGORITHM == SH_ORIGINAL:
            self.search_map[self.home[0]][self.home[1]] = 1
        elif properties.ALGORITHM == SH_TIMESTAMP:
            init_time = time.time()
            self.init_time = init_time
            self.search_map = [[init_time for j in range(int(self.mapa_largo))]for i in range(int(self.mapa_ancho))]
        elif properties.ALGORITHM == RANDOM:
            self.search_map[self.home[0]][self.home[1]] = 1
        self.ip = ip
        self.port = port
        # success = self.bebop.connect(10)
        # print(success)
        self.bebop.set_max_altitude(self.max_altitude)
        self.bebop.ask_for_state_update()
        if properties.STREAMING_MODE_ON:
            self.initializeStreaming()

    def initSearchMapWithObstacles(self):
        print('obstaculos: ', self.obstaculos)
        for obstacle in self.obstaculos:
            print('obstacle: ', obstacle)
            self.search_map[obstacle[0]][obstacle[1]] = -1

    def take_off(self):
        self.bebop.safe_takeoff(10)

    def land(self):
        self.bebop.safe_land(10)

    def move(self, new_position):
        print("new position: ", new_position)
        print("current_position: ", self.current_position)
        verticalMove = self.getDronVerticalAlignment()
        if properties.ROTATE:
            rotation_diff = utils.angleDifference(self.current_position, new_position, self.current_rotation)
            distance_diff = utils.cartesianDistance(self.current_position, new_position)
            self.bebop.move_relative(0, 0, 0, rotation_diff)
            time.sleep(2)
            self.bebop.move_relative(distance_diff, 0, verticalMove, 0)
            self.current_rotation -= rotation_diff
            time.sleep(2)
        else:
            dx, dy = new_position[0] - self.current_position[0], new_position[1] - self.current_position[1]
            real_dx, real_dy = dx * self.rango_ancho, dy * self.rango_largo
            self.bebop.move_relative(real_dx, real_dy, verticalMove, 0)
        time.sleep(2)
        self.current_position = new_position
        self.mutex_search_map.acquire()
        utils.printMatrix(self.search_map)
        self.mutex_search_map.release()

    def setPoiPosition(self, poiPosition):
        self.poi_position = poiPosition

    def explore(self, forcePosition):
        if properties.ALGORITHM == SH_ORIGINAL:
            return self.explore_sh_original(forcePosition)
        elif properties.ALGORITHM == SH_TIMESTAMP:
            return self.explore_sh_timestamp(forcePosition)
        elif properties.ALGORITHM == RANDOM:
            return self.explore_random(forcePosition)
        elif properties.ALGORITHM == SH_NO_GREEDY:
            return self.explore_sh_no_greedy2(forcePosition)

    def explore_sh_original(self, forcePosition):
        firstTime = True
        x = self.current_position[0]
        y = self.current_position[1]
        best_values = []
        for y2 in range(-1, 2):
            for x2 in range(-1, 2):
                x3 = x + x2
                y3 = y + y2
                if self.validatePosition(x3, y3, forcePosition):
                    if firstTime:
                        self.mutex_search_map.acquire()
                        val = self.search_map[x3][y3]
                        self.mutex_search_map.release()
                        firstTime = False
                    # print("x3: " + str(x3) + " y3: " + str(y3) + " self.mapa_ancho: " + str(self.mapa_ancho) + " self.mapa_largo: " + str(self.mapa_largo))
                    self.mutex_search_map.acquire()
                    if (self.search_map[x3][y3] == val):
                        best_values.append((x3, y3))
                        val = self.search_map[x3][y3]
                    elif self.search_map[x3][y3] < val:
                        best_values = [(x3, y3)]
                        val = self.search_map[x3][y3]
                    self.mutex_search_map.release()
        selected = self.selectBestValue(best_values)
        print("x: " + str(selected[0]) + " y: " + str(selected[1]))
        return selected

    def explore_sh_timestamp(self, forcePosition):
        firstTime = True
        x = self.current_position[0]
        y = self.current_position[1]
        best_values = []
        for y2 in range(-1, 2):
            for x2 in range(-1, 2):
                x3 = x + x2
                y3 = y + y2
                if self.validatePosition(x3, y3, forcePosition):
                    if firstTime:
                        self.mutex_search_map.acquire()
                        val = self.search_map[x3][y3]
                        self.mutex_search_map.release()
                        firstTime = False
                    self.mutex_search_map.acquire()
                    if (self.search_map[x3][y3] == val):
                        best_values.append((x3, y3))
                        val = self.search_map[x3][y3]
                    elif self.search_map[x3][y3] < val:
                        best_values = [(x3, y3)]
                        val = self.search_map[x3][y3]
                    self.mutex_search_map.release()
        print("BEST VALUES: ", best_values)
        selected = self.selectBestValue(best_values)
        print("x: " + str(selected[0]) + " y: " + str(selected[1]))
        return selected

    def explore_random(self, forcePosition):
        x = self.current_position[0]
        y = self.current_position[1]
        best_values = []
        for y2 in range(-1, 2):
            for x2 in range(-1, 2):
                x3 = x + x2
                y3 = y + y2
                if self.validatePosition(x3, y3, forcePosition):
                    best_values.append((x3, y3))
        selected = self.selectBestValue(best_values)
        print("x: " + str(selected[0]) + " y: " + str(selected[1]))
        return selected

    def explore_sh_no_greedy(self, forcePosition):
        firstTime = True
        x = self.current_position[0]
        y = self.current_position[1]
        best_values = []
        for y2 in range(-1, 2):
            for x2 in range(-1, 2):
                x3 = x + x2
                y3 = y + y2
                if self.validatePosition(x3, y3, forcePosition):
                    if firstTime:
                        self.mutex_search_map.acquire()
                        val = self.search_map[x3][y3]
                        self.mutex_search_map.release()
                        firstTime = False
                    self.mutex_search_map.acquire()
                    currentRegion = self.getCurrentRegion()
                    bestRegion = self.selectUnexploredRegion()
                    if self.isClosestToBestRegion(currentRegion, bestRegion, x2, y2):
                        if (self.search_map[x3][y3] == val):
                            best_values.append((x3, y3))
                            val = self.search_map[x3][y3]
                        elif self.search_map[x3][y3] < val:
                            best_values = [(x3, y3)]
                            val = self.search_map[x3][y3]
                    self.mutex_search_map.release()
        print("BEST VALUES: ", best_values)
        selected = self.selectBestValue(best_values)
        print("x: " + str(selected[0]) + " y: " + str(selected[1]))
        return selected

    def explore_sh_no_greedy2(self, forcePosition):
        if self.pathToFollow is not None and len(self.pathToFollow) > 0:
            return self.getNewPositionFromPath()
        else:
            newZone = self.isChangeZone()
            if newZone is not None:
                print("NEW ZONE: ", newZone)
                self.destinationZone = newZone
                self.getZonePath(newZone)
                # self.selectNewZone(newZone)
                return self.getNewPositionFromPath()
            else:
                return self.explore_sh_original(forcePosition)

    def getNewPositionFromPath(self):
        new_position = self.pathToFollow[0]
        del self.pathToFollow[0]
        print("self.getPositionZone(new_position): ", self.getPositionZone(new_position), " self.destinationZone: ", self.destinationZone, " self.search_map[new_position[0], new_position[1]]: ", self.search_map[new_position[0]][new_position[1]])
        if self.getPositionZone(new_position) == self.destinationZone and self.search_map[new_position[0]][new_position[1]] == 0:
            print('END NEW ZONE')
            self.pathToFollow = None
            self.destinationZone = None
        return new_position

    def isChangeZone(self):
        currentZone = self.getCurrentRegion()
        zonesCoverage = self.getZonesCoverage()
        currentZoneCoverage = zonesCoverage[currentZone - 1]
        minZoneCoverage = min(zonesCoverage)
        print("currentZone: ",currentZone," currentZoneCoverage: ",currentZoneCoverage," minZoneCoverage: ",minZoneCoverage, " zonesCoverage: ",zonesCoverage)
        if minZoneCoverage >= MIN_ACCEPTABLE_COVERAGE:
            self.countIter += 1
            zonesCoverage = self.getZonesCoverage()
            currentZoneCoverage = zonesCoverage[currentZone - 1]
            minZoneCoverage = min(zonesCoverage)
        if currentZoneCoverage >= MIN_ACCEPTABLE_COVERAGE or currentZoneCoverage - minZoneCoverage > COVERAGE_THRESHOLD:
            newZone = self.selectUnexploredRegion()
            return newZone
        return None

    def getZonePath(self, newZone):
        zonePosition = self.selectPositionInZone(newZone)
        print("self.current_position: ", self.current_position, " zonePosition: ", zonePosition)
        pathfinder = Pathfinder(self.current_position, zonePosition)
        pathToFollow = pathfinder.findPath()
        self.pathToFollow = pathfinder.parsePathToCoordinates(pathToFollow)

    def selectPositionInZone(self, zone):
        if zone == 1:
            position = (0, 0)
        elif zone == 2:
            position = (0, int(self.mapa_largo - 1))
        elif zone == 3:
            position = (int(self.mapa_ancho - 1), 0)
        else:
            position = (int(self.mapa_ancho - 1), int(self.mapa_largo - 1))
        # if zone == 1 or zone == 2:
        #     while position[0] < self.mapa_ancho and self.search_map[position[0], position[1]] == -1:
        #         position = (position[0] + 1, 0)
        # elif zone == 3 or zone == 4:
        #     while position[0] < self.mapa_largo and self.search_map[position[0], position[1]] == -1:
        #         position = (0, position[1] + 1)
        # asumo que encuentro posicion valida
        return position

    def selectNewZone(self, currentZone):
        newZone = random.randint(0, 3)
        while newZone == currentZone:
            newZone = random.randint(0, 3)
        return newZone

    def selectNewZone2(self, currentZone):
        newZone = random.randint(0, 3)
        while newZone == currentZone:
            newZone = random.randint(0, 3)
        return newZone

    def isClosestToBestRegion(currentRegion, bestRegion, x, y):
        if currentRegion == bestRegion:
            return True
        bestCoordinates = getBestCoordinates(currentRegion, bestRegion)
        if x in bestCoordinates[0] and y in bestCoordinates[1]:
            return True
        return False

    def getBestCoordinates(currentRegion, bestRegion):
        if currentRegion == 1:
            if bestRegion == 2:
                return [(-1, 1), (0, 1), (1, 1)]
            elif bestRegion == 3:
                return [(1, -1), (1, 0), (1, 1)]
            else:
                return [(0, 1), (1, 1), (1, 0)]
        elif currentRegion == 2:
            if bestRegion == 1:
                return [(-1, -1), (0, -1), (1, 1)]
            elif bestRegion == 3:
                return [(1, -1), (0, -1), (1, 0)]
            else:
                return [(1, -1), (1, 0), (1, 1)]
        elif currentRegion == 3:
            if bestRegion == 1:
                return [(-1, -1), (-1, 0), (-1, 1)]
            elif bestRegion == 2:
                return [(-1, 0), (-1, 1), (0, 1)]
            else:
                return [(-1, 1), (0, 1), (1, 1)]
        else:
            if bestRegion == 1:
                return [(-1, -1), (-1, 0), (0, -1)]
            elif bestRegion == 2:
                return [(-1, -1), (-1, 0), (-1, 1)]
            else:
                return [(-1, -1), (0, -1), (1, -1)]

    def getCurrentRegion(self):
        print("getCurrentRegion")
        return self.getPositionZone(self.current_position)

    def getPositionZone(self, position):
        print("position: ",position," self.mapa_largo: ",self.mapa_largo, " self .mapa_ancho: ", self .mapa_ancho)
        if self.mapa_largo / 2 > position[1] and self .mapa_ancho / 2 > position[0]:
            return 1
        elif self.mapa_largo / 2 <= position[1] and self .mapa_ancho / 2 > position[0]:
            return 2
        elif self.mapa_largo / 2 > position[1] and self .mapa_ancho / 2 <= position[0]:
            return 3
        elif self.mapa_largo / 2 <= position[1] and self .mapa_ancho / 2 <= position[0]:
            return 4

    def selectUnexploredRegion(self):
        regionCoverage = []
        regionCoverage.append(getMapCoverage(self, 0, self.mapa_ancho / 2, 0, self.mapa_largo / 2))
        regionCoverage.append(getMapCoverage(self, self.mapa_ancho / 2, self.mapa_ancho, 0, self.mapa_largo / 2))
        regionCoverage.append(getMapCoverage(self, 0, self.mapa_ancho / 2, self.mapa_largo / 2, self.mapa_largo))
        regionCoverage.append(getMapCoverage(self, self.mapa_ancho / 2, self.mapa_ancho, self.mapa_largo / 2, self.mapa_largo))
        return regionCoverage.index(min(regionCoverage)) + 1

    def getZonesCoverage(self):
        regionCoverage = []
        regionCoverage.append(getMapCoverage(self, 0, self.mapa_ancho / 2, 0, self.mapa_largo / 2))
        regionCoverage.append(getMapCoverage(self, self.mapa_ancho / 2, self.mapa_ancho, 0, self.mapa_largo / 2))
        regionCoverage.append(getMapCoverage(self, 0, self.mapa_ancho / 2, self.mapa_largo / 2, self.mapa_largo))
        regionCoverage.append(getMapCoverage(self, self.mapa_ancho / 2, self.mapa_ancho, self.mapa_largo / 2, self.mapa_largo))
        return regionCoverage

    def selectBestValue(self, best_values):
        lenght = len(best_values)
        # print("selectBestValue: " + str(lenght))
        if(lenght == 1):
            return best_values[0]
        else:
            selected = random.randint(0, lenght - 1)
            return best_values[selected]

    def validatePosition(self, x3, y3, forcePosition):
        condition = x3 >= 0 and y3 >= 0 and x3 < self.mapa_ancho and y3 < self.mapa_largo
        tupla = (x3, y3)
        if self.pointIsObstacule(x3, y3):
            return False
        elif (forcePosition is not None):
            return (condition and self.minDistanceToTarget(self.home, self.current_position, tupla))
        elif self.poi_position is not None:
            return (condition and self.minDistanceToTarget(self.poi_position, self.current_position, tupla))
        elif self.checkBatteryStatus() == NORMAL:
            return condition
        else:
            return (condition and self.minDistanceToTarget(self.home, self.current_position, tupla))

    def minDistanceToTarget(self, target, positionA, positionB):
        # print("minDistanceToTarget")
        distance2 = self.calculateDistance(target, positionA)
        distance1 = self.calculateDistance(target, positionB)
        # print("distance1: " + str(distance1) + " distance2: " + str(distance2))
        return (distance1 <= distance2)

    def pointIsObstacule(self, x1, x2):
        isObstacule = False
        for obs in self.obstaculos:
            if obs[0] == x1 and obs[1] == x2:
                isObstacule = True
        return isObstacule

    def calculateDistance(self, tuple1, tuple2):
        return math.sqrt((tuple2[1] - tuple1[1])**2 + (tuple2[0] - tuple1[0])**2)

    def updateSearchMap(self, tupla):
        self.mutex_search_map.acquire()
        if properties.ALGORITHM == SH_ORIGINAL or properties.ALGORITHM == SH_NO_GREEDY:
            self.search_map[tupla[0]][tupla[1]] += 1
        elif properties.ALGORITHM == SH_TIMESTAMP:
            self.search_map[tupla[0]][tupla[1]] = time.time()
        elif properties.ALGORITHM == RANDOM:
            self.search_map[tupla[0]][tupla[1]] += 1
        self.mutex_search_map.release()

    def getSearchMap(self):
        # self.mutex_search_map.acquire()
        return [[self.search_map[i][j] for j in range(int(self.mapa_largo))]for i in range(int(self.mapa_ancho))]
        # self.mutex_search_map.release()

    def getDroneAltitude(self):
        print("altura", self.bebop.sensors.sensors_dict["AltitudeChanged_altitude"])
        return self.bebop.sensors.sensors_dict["AltitudeChanged_altitude"]

    def checkDroneAltitudeStatus(self):
        altitude = self.getDroneAltitude()
        if (altitude < properties.MIN_ALTITUDE):
            return TOO_LOW
        elif (altitude > properties.MAX_ALTITUDE):
            return TOO_HIGH
        else:
            return ALTITUDE_OK

    def getDronVerticalAlignment(self):
        droneAltitudeStatus = self.checkDroneAltitudeStatus()
        verticalAlignment = 0
        if (droneAltitudeStatus == TOO_LOW or droneAltitudeStatus == TOO_HIGH):
            # negative goes up, positive goes down
            verticalAlignment = self.getDroneAltitude() - properties.OPTIMAL_ALTITUDE
        else:
            verticalAlignment = 0
        return verticalAlignment

    def getBatteryPercentage(self):
        return self.bebop.sensors.battery

    def checkBatteryStatus(self):
        batteryPercentage = self.getBatteryPercentage()
        if batteryPercentage < 5:
            return CRITICAL
        elif batteryPercentage < 10:
            return LOW
        else:
            return NORMAL

    def goHome(self):
        pathfinder = Pathfinder(self.current_position, self.home)
        pathToFollow = pathfinder.findPath()
        pathfinder.printFinalMap()
        for nextPosition in pathfinder.parsePathToCoordinates(pathToFollow):
            self.move(nextPosition)

    def getClosestCoordinateToTarget(self, target, pos):
        res = self.current_position[pos]
        if res < target[pos]:
            res = res + 1
        elif res > target[pos]:
            res = res - 1
        return res

    def moveToPoiCritico(self, path):
        for nextPosition in path:
            self.move(nextPosition)

    def moveNextPositionPOICritico(self, new_position):
        dx, dy = new_position[0] - self.current_position[0], new_position[1] - self.current_position[1]
        real_dx, real_dy = dx * self.rango_ancho, dy * self.rango_largo
        verticalMove = self.getDronVerticalAlignment()
        self.bebop.move_relative(real_dx, real_dy, verticalMove, 0)
        time.sleep(2)
        self.current_position = new_position

    def disconnect(self):
        if properties.STREAMING_MODE_ON:
            self.closeStreaming()
        self.bebop.disconnect()

    def initializeStreaming(self):
        print("-- Starting Streaming... --")
        self.bebop.set_video_resolutions('rec720_stream720')
        self.bebop.start_video_stream()
        print("-- Streaming Started! --")

    def closeStreaming(self):
        print("-- Stopping Streaming... --")
        self.bebop.stop_video_stream()
        print("-- Streaming stopped!")
