import properties
import utils
import math
from batteryEnum import LOW, CRITICAL, NORMAL
import threading
from pyparrot.Bebop import Bebop
import random
import time


class drone:
    def __init__(self, home):
        self.rango_largo = properties.RANGO_LARGO
        self.rango_ancho = properties.RANGO_ANCHO
        self.mapa_largo = properties.MAPA_LARGO / self.rango_largo
        self.mapa_ancho = properties.MAPA_ANCHO / self.rango_ancho
        self.ip = None
        self.search_map = [[0 for j in range(int(self.mapa_largo))]for i in range(int(self.mapa_ancho))]
        self.current_position = home
        self.mutex_search_map = threading.Lock()
        self.poi_position = None
        self.home = home
        self.bebop = Bebop()
        self.obstaculos = properties.OBSTACLES

    def initialize(self, ip):
        self.search_map[self.home[0]][self.home[1]] = 1
        self.ip = ip
        success = self.bebop.connect(10)
        print(success)
        self.bebop.ask_for_state_update()

    def take_off(self):
        self.bebop.safe_takeoff(10)

    def land(self):
        self.bebop.safe_land(10)

    def move(self, new_position):
        dx, dy = new_position[0] - self.current_position[0], new_position[1] - self.current_position[1]
        real_dx, real_dy = dx * self.rango_ancho, dy * self.rango_largo
        self.bebop.move_relative(real_dx, real_dy, 0, 0)
        time.sleep(2)
        self.current_position = new_position
        self.mutex_search_map.acquire()
        utils.printMatrix(self.search_map)
        self.mutex_search_map.release()

    def setPoiPosition(self, poiPosition):
        self.poi_position = poiPosition

    def explore(self, forcePosition):
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
                        best_values = []
                        best_values.append((x3, y3))
                        val = self.search_map[x3][y3]
                    self.mutex_search_map.release()
        selected = self.selectBestValue(best_values)
        print("x: " + str(selected[0]) + " y: " + str(selected[1]))
        return selected

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
        if (forcePosition is not None):
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

    def pointIsObstacule(x1, x2):
        isObstacule = False
        for obs in self.obstaculos:
            if obs[0] == x1 and obs[1] == x2 :
                isObstacule = True
        return isObstacule

    def calculateDistance(self, tuple1, tuple2):
        return math.sqrt((tuple2[1] - tuple1[1])**2 + (tuple2[0] - tuple1[0])**2)

    def updateSearchMap(self, tupla):
        self.mutex_search_map.acquire()
        self.search_map[tupla[0]][tupla[1]] += 1
        self.mutex_search_map.release()

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
        self.move(self.home)

    def getClosestCoordinateToTarget(self, target, pos):
        res = self.current_position[pos]
        if res < target[pos]:
            res = res + 1
        elif res > target[pos]:
            res = res - 1
        return res

    def getClosestPositionToTarget(self, target):
        x1 = getClosestCoordinateToTarget(target, 0)
        x2 = getClosestCoordinateToTarget(target, 1)
        position = (x1, x2)
        return position


    def moveToPoiCritico(self, path):
        for i in range(len(path)):
            nextPosition = path[i]
            self.moveNextPositionPOICritico(nextPosition)


    def moveNextPositionPOICritico(self, new_position):
        dx, dy = new_position[0] - self.current_position[0], new_position[1] - self.current_position[1]
        real_dx, real_dy = dx * self.rango_ancho, dy * self.rango_largo
        self.bebop.move_relative(real_dx, real_dy, 0, 0)
        time.sleep(2)
        self.current_position = new_position

    def disconnect(self):
        self.bebop.disconnect()
