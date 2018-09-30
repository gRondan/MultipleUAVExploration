from threading import Timer
from utils import getStringMatrix, convertTupleToString
import time


class stats:
    def __init__(self, drone, id):
        self.drone = drone
        self.logFile = open("log" + str(id) + ".txt", "w+")
        self.timer = Timer(10, self.registerData)
        self.timer.start()
        self.iteration = 1
        self.poiVigilarTimers = dict({})
        self.poiCriticoTimers = dict({})

    def registerData(self):
        print("log Mapa####################")
        searchMap = self.drone.getSearchMap()
        self.logFile.write("\n Iteration: " + str(self.iteration) + "\n")
        self.logFile.write(getStringMatrix(searchMap))
        self.logFile.write("\n")
        mapCoverage = self.getMapCoverage(searchMap)
        self.logFile.write("Map Coverage: " + str(mapCoverage) + "\n")
        self.iteration += 1
        self.timer = Timer(10, self.registerData)
        self.timer.start()

    def getMapCoverage(self, searchMap):
        totalMap = self.drone.mapa_largo * self.drone.mapa_ancho
        isTimer = self.drone.init_time is not None
        contSinExplorar = 0
        for i in range(int(self.drone.mapa_largo)):
            for j in range(int(self.drone.mapa_ancho)):
                if isTimer:
                    if searchMap[i][j] != self.drone.init_time:
                        contSinExplorar += 1
                elif searchMap[i][j] > 0:
                    contSinExplorar += 1
        return (contSinExplorar * 100) // totalMap

    def poiVigilarTimeout(self, poi):
        self.poiVigilarTimers[convertTupleToString(poi)] = time.time()

    def poiCriticoTimeout(self, poi):
        self.poiCriticoTimers[convertTupleToString(poi)] = time.time()

    def poiExplorado(self, poiKey):
        if poiKey in self.poiVigilarTimers:
            self.logFile.write("Poi vigilado: " + poiKey + " Tiempo respuesta: " + str(time.time() - self.poiVigilarTimers[poiKey]) + "\n")
            del self.poiVigilarTimers[poiKey]
        if poiKey in self.poiCriticoTimers:
            self.logFile.write("Poi Critico vigilado: " + poiKey + " Tiempo respuesta: " + str(time.time() - self.poiCriticoTimers[poiKey]) + "\n")
            del self.poiCriticoTimers[poiKey]

    def endExecution(self):
        self.logFile.close()
