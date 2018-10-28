from threading import Timer
from utils import getStringMatrix, convertTupleToString, getMapCoverage
from pyparrot.networking.connectionProperties import ACTIVATE_LOG, LOG_NAME
from properties import OBSTACLES, ALGORITHM
import time
import sys
import csv


class stats:
    def __init__(self, drone):
        if ACTIVATE_LOG is not None and ACTIVATE_LOG is True:
            self.drone = drone
            try:
                self.executionId = sys.argv[1]
            except:
                self.executionId = 1
            try:
                self.instanceId = sys.argv[2]
            except:
                self.instanceId = 1
            self.algorithm = ALGORITHM
            # self.logFile = open("log" + str(executionId) + ".txt", "w+")
            self.csvLogFile = "log/log" + str(LOG_NAME) + ".csv"
            self.csvLogPoiFile = "log/logPOI" + str(LOG_NAME) + ".csv"
            self.csvLogMap = "log/logMap" + str(LOG_NAME) + str(self.executionId) + str(self.instanceId) + self.algorithm + ".csv"
            self.logMapTimestamp = "log/logMapTimestamp" + str(LOG_NAME) + str(self.executionId) + str(self.instanceId) + self.algorithm + ".csv"
            self.timer = Timer(10, self.registerData)
            self.timer.start()
            self.iteration = 1
            self.poiVigilarTimers = dict({})
            self.poiCriticoTimers = dict({})
            self.poiVigilarTiempoAtencion = dict({})
            self.poiCriticoTiempoAtencion = dict({})
            self.cantPoiVigilar = 0
            self.cantPoiCritico = 0
            self.poiVigilarTotal = 0
            self.poiCriticoTotal = 0
            self.poiVigilarTotalTimersActivados = 0
            self.poiCriticoTotalTimersActivados = 0
            self.poiVigilarPeorCaso = 0
            self.poiCriticoPeorCaso = 0
            self.poiVigilarMejorCaso = 0
            self.poiCriticoMejorCaso = 0
            self.coverage = []

    def registerData(self):
        if ACTIVATE_LOG is not None and ACTIVATE_LOG is True:
            # print("log Mapa####################")
            searchMap = self.drone.getSearchMap()
            # self.logFile.write("\n Iteration: " + str(self.iteration) + "\n")
            # self.logFile.write(getStringMatrix(searchMap))
            # self.logFile.write("\n")
            mapCoverage = getMapCoverage(self.drone, 0, self.drone.mapa_ancho, 0, self.drone.mapa_largo)
            # self.logFile.write("Map Coverage: " + str(mapCoverage) + "\n")
            self.iteration += 1
            self.coverage.append(mapCoverage)
            self.timer = Timer(10, self.registerData)
            self.timer.start()

    def getMapCoverage(self, searchMap):
        if ACTIVATE_LOG is not None and ACTIVATE_LOG is True:
            totalMap = self.drone.mapa_largo * self.drone.mapa_ancho
            isTimer = self.drone.init_time is not None
            totalMap -= len(OBSTACLES)
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
        if ACTIVATE_LOG is not None and ACTIVATE_LOG is True:
            poiKey = convertTupleToString(poi)
            self.poiVigilarTimers[poiKey] = time.time()
            self.poiVigilarTotalTimersActivados += 1
            if poiKey not in self.poiVigilarTiempoAtencion:
                self.poiVigilarTiempoAtencion[poiKey] = []

    def poiCriticoTimeout(self, poi):
        if ACTIVATE_LOG is not None and ACTIVATE_LOG is True:
            poiKey = convertTupleToString(poi)
            self.poiCriticoTimers[convertTupleToString(poi)] = time.time()
            self.poiCriticoTotalTimersActivados += 1
            if poiKey not in self.poiCriticoTiempoAtencion:
                self.poiCriticoTiempoAtencion[poiKey] = []

    def poiExplorado(self, poiKey):
        if ACTIVATE_LOG is not None and ACTIVATE_LOG is True:
            if poiKey in self.poiVigilarTimers:
                tiempoRespuesta = time.time() - self.poiVigilarTimers[poiKey]
                # self.logFile.write("Poi vigilado: " + poiKey + " Tiempo respuesta: " + str(tiempoRespuesta) + "\n")
                del self.poiVigilarTimers[poiKey]
                if self.cantPoiVigilar == 0 or tiempoRespuesta < self.poiVigilarMejorCaso:
                    self.poiVigilarMejorCaso = tiempoRespuesta
                if self.cantPoiVigilar == 0 or tiempoRespuesta > self.poiVigilarPeorCaso:
                    self.poiVigilarPeorCaso = tiempoRespuesta
                self.cantPoiVigilar += 1
                self.poiVigilarTotal += tiempoRespuesta
                self.poiVigilarTiempoAtencion[poiKey].append(tiempoRespuesta)
            if poiKey in self.poiCriticoTimers:
                tiempoRespuesta = time.time() - self.poiCriticoTimers[poiKey]
                # self.logFile.write("Poi Critico vigilado: " + poiKey + " Tiempo respuesta: " + str(tiempoRespuesta) + "\n")
                del self.poiCriticoTimers[poiKey]
                if self.cantPoiCritico == 0 or tiempoRespuesta < self.poiCriticoMejorCaso:
                    self.poiCriticoMejorCaso = tiempoRespuesta
                if self.cantPoiCritico == 0 or tiempoRespuesta > self.poiCriticoPeorCaso:
                    self.poiCriticoPeorCaso = tiempoRespuesta
                self.cantPoiCritico += 1
                self.poiCriticoTotal += tiempoRespuesta
                self.poiCriticoTiempoAtencion[poiKey].append(tiempoRespuesta)

    def endExecution(self):
        if ACTIVATE_LOG is not None and ACTIVATE_LOG is True:
            self.timer.cancel()
            # self.logFile.write("####END EXECUTION####")
            self.registerData()
            self.timer.cancel()
            with open(self.csvLogFile, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                # self.logFile.write("PoiCritico cantidad pois activados: " + str(self.poiCriticoTotalTimersActivados) + "\n")
                # self.logFile.write("PoiVigilar cantidad pois atendidos: " + str(self.cantPoiVigilar) + "\n")
                # self.logFile.write("PoiCritico cantidad pois atendidos: " + str(self.cantPoiCritico) + "\n")
                # self.logFile.write("PoiVigilar cantidad pois activados: " + str(self.poiVigilarTotalTimersActivados) + "\n")
                poiVigilarPromedio = 0
                poiCriticoPromedio = 0
                if self.cantPoiVigilar > 0:
                    poiVigilarPromedio = self.poiVigilarTotal / self.cantPoiVigilar
                if self.cantPoiCritico > 0:
                    poiCriticoPromedio = self.poiCriticoTotal / self.cantPoiCritico
                # self.logFile.write("PoiVigilar tiempoRespuesta promedio: " + str(poiVigilarPromedio) + "\n")
                # self.logFile.write("PoiCritico tiempoRespuesta promedio: " + str(poiCriticoPromedio) + "\n")
                # self.logFile.write("PoiVigilar tiempoRespuesta peor caso: " + str(self.poiVigilarPeorCaso) + "\n")
                # self.logFile.write("PoiCritico tiempoRespuesta peor caso: " + str(self.poiCriticoPeorCaso) + "\n")
                # self.logFile.write("PoiVigilar tiempoRespuesta mejor caso: " + str(self.poiVigilarMejorCaso) + "\n")
                # self.logFile.write("PoiCritico tiempoRespuesta mejor caso: " + str(self.poiCriticoMejorCaso) + "\n")
                # if self.executionId == 1:
                # writer.writerow(["Ejecucion", "Instancia", "Algoritmo", "Total map coverage", "map coverage by time (10s)", "PoiVigilar cantidad pois activados", "PoiCritico cantidad pois activados", "PoiVigilar cantidad pois atendidos", "PoiCritico cantidad pois atendidos", "PoiVigilar tiempoRespuesta promedio", "PoiCritico tiempoRespuesta promedio", "PoiVigilar tiempoRespuesta peor caso", "PoiCritico tiempoRespuesta peor caso", "PoiVigilar tiempoRespuesta mejor caso", "PoiCritico tiempoRespuesta mejor caso"])
                totalCoverage = self.coverage[-1]
                # print("#########" + str(self.coverage))
                self.coverage.remove(totalCoverage)
                writer.writerow([self.executionId, self.instanceId, self.algorithm, totalCoverage, self.coverage, self.poiVigilarTotalTimersActivados, self.poiCriticoTotalTimersActivados, self.cantPoiVigilar, self.cantPoiCritico, poiVigilarPromedio, poiCriticoPromedio, self.poiVigilarPeorCaso, self.poiCriticoPeorCaso, self.poiVigilarMejorCaso, self.poiCriticoMejorCaso])
                with open(self.csvLogPoiFile, 'a', newline='') as csvfile2:
                    writerPoi = csv.writer(csvfile2, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    # if self.executionId == 1:
                    # writerPoi.writerow(["Ejecucion", "Instancia", "Algoritmo", "Poi position", "Poi Type", "Poi tiempos"])
                    for poiKey in self.poiVigilarTiempoAtencion:
                        writerPoi.writerow([self.executionId, self.instanceId, self.algorithm, poiKey, "Vigilar"] + self.poiVigilarTiempoAtencion[poiKey])
                        # self.logFile.write("PoiVigilar " + poiKey + " tiempos respuesta: " + str(self.poiVigilarTiempoAtencion[poiKey]) + "\n")
                        # if self.poiVigilarTiempoAtencion:
                        #     total = 0
                        #     total += [i for i in self.poiVigilarTiempoAtencion]
                        #     promedio = total / len(self.poiVigilarTiempoAtencion)
                        #     self.logFile.write("PoiVigilar: " + poiKey + " tiempo promedio: " + str(promedio) + "\n")
                    for poiKey in self.poiCriticoTiempoAtencion:
                        writerPoi.writerow([self.executionId, self.instanceId, self.algorithm, poiKey, "Critico"] + self.poiCriticoTiempoAtencion[poiKey])
                        # self.logFile.write("PoiCritico " + poiKey + " tiempos respuesta: " + str(self.poiCriticoTiempoAtencion[poiKey]) + "\n")
                        # if self.poiCriticoTiempoAtencion:
                        #     total = 0
                        #     total += [i for i in self.poiCriticoTiempoAtencion]
                        #     promedio = total / len(self.poiCriticoTiempoAtencion)
                        #     self.logFile.write("PoiCritico: " + poiKey + " tiempo promedio: " + str(promedio) + "\n")
                with open(self.csvLogMap, 'a', newline='') as csvfile3:
                    writerLogMap = csv.writer(csvfile3, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    for j in range(int(self.drone.mapa_largo)):
                        row = ""
                        for i in range(int(self.drone.mapa_ancho)):
                            if ((i, j) in OBSTACLES):
                                row += "X;"
                            else:
                                row += str(self.drone.logMap[i][j]) + ";"
                        writerLogMap.writerow([row])
                currentTime = time.time()
                with open(self.logMapTimestamp, 'a', newline='') as csvfile4:
                    writerLogTimestampMap = csv.writer(csvfile4, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    # print(OBSTACLES)
                    for j in range(0, int(self.drone.mapa_largo)):
                        row = ""
                        for i in range(0, int(self.drone.mapa_ancho)):
                            if (self.drone.pointIsObstacule(i, j)):
                                row += "X;"
                            else:
                                row += str(int(round(currentTime - self.drone.logMapTimestamp[i][j]))) + ";"
                        writerLogTimestampMap.writerow([row])
            # self.logFile.close()
            print("END LOG")
