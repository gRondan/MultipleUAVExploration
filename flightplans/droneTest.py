import properties
import utils
import math
from random import randint
from batteryEnum import LOW, CRITICAL, NORMAL
import threading
from pyparrot.Bebop import Bebop
import random

class droneTest:
    def __init__(self, home):
        self.rango_largo = properties.RANGO_LARGO
        self.rango_ancho = properties.RANGO_ANCHO
        self.mapa_largo = properties.MAPA_LARGO/self.rango_largo
        self.mapa_ancho = properties.MAPA_ANCHO/self.rango_ancho
        self.search_map = [[0 for j in range(int(self.mapa_largo))]for i in range(int(self.mapa_ancho))]
        self.home = home
        self.current_position = home
        self.battery_status = NORMAL
        self.mutex_search_map = threading.Lock()
        self.bebop = Bebop()
        self.initialize()

    def initialize(self):
        self.search_map[self.home[0]][self.home[1]] = 1
        #success = self.bebop.connect(10)
        #print(success)
        #self.bebop.ask_for_state_update()

    def take_off(self):
        #self.bebop.safe_takeoff(10)
        print("take_off")

    def land(self):
        print("land")
        #self.bebop.safe_land(10)

    def move(self, new_position):
        dx, dy = new_position[0] - self.current_position[0], new_position[1] - self.current_position[1]
        real_dx, real_dy = dx*self.rango_ancho, dy*self.rango_largo
        #self.bebop.move_relative(real_dx, real_dy, 0, 0)
        #time.sleep(2)
        self.current_position = new_position
        self.updateSearchMap(self.current_position)
        self.mutex_search_map.acquire()
        utils.printMatrix(self.search_map)
        self.mutex_search_map.release()

    def explore(self):

        #self.updateSearchMap(self.current_position)
        exitloop = False
        firstTime = True
        x = self.current_position[0]
        y = self.current_position[1]
        best_values = []
        for y2 in range(-1,2):
            for x2 in range(-1,2):
                x3 = x+x2
                y3 = y+y2
                if self.validatePosition(x3, y3):
                    if firstTime:
                        self.mutex_search_map.acquire()
                        val = self.search_map[x3][y3]
                        self.mutex_search_map.release()
                        x1 = x3
                        y1 = y3
                        firstTime = False
                    print("x3: "+str(x3)+ " y3: "+str(y3)+" self.mapa_ancho: "+str(self.mapa_ancho)+ " self.mapa_largo: "+ str(self.mapa_largo))
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
        print("x: "+str(selected[0])+" y: "+str(selected[1]))
        return selected


    def selectBestValue(self, best_values):
        lenght = len(best_values)
        if(lenght == 1):
            return best_values[0]
        else:
            selected = random.randint(0, lenght-1)
            return best_values[selected]

    def validatePosition(self, x3, y3):
        condition = x3>=0 and y3>= 0 and x3<self.mapa_ancho and y3<self.mapa_largo
        if self.battery_status == NORMAL:
            return condition
        else:
            tupla = (x3,y3)
            distance2 = self.calculateDistance(self.home, self.current_position)
            distance1 = self.calculateDistance(self.home, tupla)
            print("distance1: "+str(distance1)+ " distance2: "+ str(distance2))
            return (condition and ( distance1 < distance2 ))

    def calculateDistance(self, tuple1, tuple2):
        return math.sqrt((tuple2[1] - tuple1[1])**2 + (tuple2[0] - tuple1[0])**2)

    def updateSearchMap(self, tupla):
        self.mutex_search_map.acquire()
        self.search_map[tupla[0]][tupla[1]] +=1
        self.mutex_search_map.release()

    def getBatteryPercentage():
        return NORMAL


    def actualizarPosicion(self):
        status = self.checkBatteryStatus()
        self.battery_status = status

        if status != CRITICAL:
            self.explore()
        else:
            self.goHome()

    def checkBatteryStatus(self):
        batteryPercentage = self.getBatteryPercentage()
        if  batteryPercentage < 5:
            return CRITICAL
        elif  batteryPercentage < 10:
            return LOW
        else:
            return NORMAL

    def goHome(self):
        x1 = self.getNewCoordinate(0)
        y1 = self.getNewCoordinate(1)
        self.current_position = (x1,y1)
        self.updateSearchMap(self.current_position)
        self.mutex_search_map.acquire()
        utils.printMatrix(self.search_map)
        self.mutex_search_map.release()


    def getNewCoordinate(self, pos):
        x1 = self.current_position[pos]
        if self.current_position[pos] < self.home[pos]:
            x1 = self.current_position[pos] + 1
        elif self.current_position[pos] > self.home[pos]:
            x1 = self.current_position[pos]-1
        return x1
