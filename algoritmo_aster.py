#
#	Implementacion de algoritmo A*
#	
#	Se utiliza un funcion heuristica f(n) para evaluar y etiquetar los nodos de la red. Esta funcion 
#	evaluara la probabilidad de un nodo de pertenecer al camino optimo.
#	
#		f(n) = g(n) + h(n)

#		g(n) = distancia actual desde el nodo origen al nodo n a etiquetar
#		h(n) = distancia estimada desde el nodo a etiquetar n al nodo destino

#	h(n) es una funcion heuristica. Expresa la idea de cuan lejos aun se esta de alcanzar el nodo destino.
#	f(n) expresa la probabilidad del nodo n de estar en el camino mas corto. Cuanto menor sea el valor de
#	esta funcion para un nodo, mas probable sera que el camino mas corto atraviese ese nodo (puede
#	considerarse como el costo de ir por el nodo n).

#	Como funcion h(n) se suele utilizar la funcion heuristica Distancia Manhattan
#	(https://es.wikipedia.org/wiki/Geometr%C3%ADa_del_taxista)

import properties
from operator import attrgetter

class Pathfinder:
	def __init__(self, init, target):
		self.rango_largo = properties.RANGO_LARGO
		self.rango_ancho = properties.RANGO_ANCHO
		self.mapa_largo = properties.MAPA_LARGO / self.rango_largo
		self.mapa_ancho = properties.MAPA_ANCHO / self.rango_ancho
		self.obstaculos = properties.OBSTACLES
		self.init = init
		self.target = target
		self.completeMap = self.initializeMap()
		self.printInitialMap()


	def printInitialMap(self):
		print("**** MAPA INICIAL *****")
		for x in range(int(self.mapa_ancho)):
			linea = " "
			for y in range(int(self.mapa_largo)):
				if self.completeMap[x][y]["isObstacle"]:
					linea = linea + "X "
				elif self.init[0] == self.completeMap[x][y]["x"] and self.init[1] == self.completeMap[x][y]["y"]:
					linea = linea + "I "
				elif self.target[0] == self.completeMap[x][y]["x"] and self.target[1] == self.completeMap[x][y]["y"]:
					linea = linea + "T "
				else:
					linea = linea + "0 "
			print(linea)
		print("************************")


	def printFinalMap(self):
		print("**** MAPA FINAL CON CAMINO *****")
		puntosEncontrados = 0
		for x in range(int(self.mapa_ancho)):
			linea = " "
			for y in range(int(self.mapa_largo)):
				esParteDelPath = False
				for z in range(len(self.pathResult)):
					if self.pathResult[z]["x"] == x and self.pathResult[z]["y"] == y:
						esParteDelPath = True
						puntosEncontrados = puntosEncontrados + 1
				if esParteDelPath:
					linea = linea + str(puntosEncontrados) + " "
				elif self.completeMap[x][y]["isObstacle"]:
					linea = linea + "X "
				elif self.init[0] == self.completeMap[x][y]["x"] and self.init[1] == self.completeMap[x][y]["y"]:
					linea = linea + "I "
				elif self.target[0] == self.completeMap[x][y]["x"] and self.target[1] == self.completeMap[x][y]["y"]:
					linea = linea + "T "
				else:
					linea = linea + "0 "
			print(linea)
		print("************************")


	def initializeMap(self):
		completeMap = [[0 for j in range(int(self.mapa_largo))]for i in range(int(self.mapa_ancho))]
		for x in range(int(self.mapa_ancho)):
			for y in range(int(self.mapa_largo)):
				completeMap[x][y] = {
				"g": 0,
				"h": 0,
				"f": 0,
				"isObstacle": self.isObstacle((x,y), False),
				"dad": None,
				"x": x,
				"y": y
				}
		self.obstaculos = properties.OBSTACLES
		return completeMap
    

	def isObstacle(self, point, removeObstacle):
		isObstacle = False
		obstacleToDelete = None
		for x in range(len(self.obstaculos)):
			obstaculo = self.obstaculos[x]
			if obstaculo[0] == point[0] and obstaculo[1] == point[1]:
				isObstacle = True
				if removeObstacle:
					obstacleToDelete = x
		if isObstacle and removeObstacle:
			del self.obstaculos[obstacleToDelete]
		return isObstacle


	def manhattanDistance(self, init, target):
		return (abs(init["x"] - target["x"]) + abs(init["y"] - target["y"]))


	def getMapNode(self, x, y):
		return self.completeMap[x][y]


	def getNeighbours(self, point):
		neighbours = []
		if ((point["x"] - 1) >= 0 and not self.completeMap[point["x"] - 1][point["y"]]["isObstacle"]):
			neighbours.append(self.getMapNode(point["x"] - 1, point["y"]))
			if ((point["y"] - 1 >= 0) and not self.completeMap[point["x"] - 1][point["y"] - 1]["isObstacle"]):
				neighbours.append(self.getMapNode(point["x"] - 1, point["y"] - 1))
			if ((point["y"] + 1 < self.mapa_ancho) and not self.completeMap[point["x"] - 1][point["y"] + 1]["isObstacle"]):
				neighbours.append(self.getMapNode(point["x"] - 1, point["y"] + 1))
		if ((point["x"] + 1) < self.mapa_largo and not self.completeMap[point["x"] + 1][point["y"]]["isObstacle"]):
			neighbours.append(self.getMapNode(point["x"] + 1, point["y"]))
			if ((point["y"] - 1 >= 0) and not self.completeMap[point["x"] + 1][point["y"] - 1]["isObstacle"]):
				neighbours.append(self.getMapNode(point["x"] + 1, point["y"] - 1))
			if ((point["y"] + 1 < self.mapa_ancho) and not self.completeMap[point["x"] + 1][point["y"] + 1]["isObstacle"]):
				neighbours.append(self.getMapNode(point["x"] + 1, point["y"] + 1))
		if ((point["y"] - 1 >= 0) and not self.completeMap[point["x"]][point["y"] - 1]["isObstacle"]):
			neighbours.append(self.getMapNode(point["x"], point["y"] - 1))
		if ((point["y"] + 1 < self.mapa_ancho) and not self.completeMap[point["x"]][point["y"] + 1]["isObstacle"]):
			neighbours.append(self.getMapNode(point["x"], point["y"] + 1))
		return neighbours


	def printNeighbours(self, node, neighbours):
		vecinos = "==>Vecinos de (" + str(node["x"]) + "," + str(node["y"]) + "):  "
		for i in range(len(neighbours)):
			vecinos = vecinos + "(" + str(neighbours[i]["x"]) + "," + str(neighbours[i]["y"]) + ")"
		print(vecinos)


	def arrivedToTarget(self, point, target):
		return (point["x"] == target[0] and point["y"] == target[1])


	def calculateG(self, point, target):
		node = self.completeMap[point["x"]][point["y"]]
		if point["x"] != target["x"] and point["y"] != target["y"]:
			# movimiento diagonal, costo=14
			return node["g"] + 14
		else:
			# movimiento horizontal o vertical, costo=10
			return node["g"] + 10

	def setParentAndRecalculateFactors(self, node, adyacent, newG):
		adyacentNode = self.completeMap[adyacent["x"]][adyacent["y"]]
		# print("DAD TO ASSIGN: " + str(self.completeMap[node["x"]][node["y"]]))
		adyacentNode["dad"] = self.completeMap[node["x"]][node["y"]]
		adyacentNode["g"] = newG
		adyacentNode["h"] = self.manhattanDistance(adyacent, self.completeMap[self.target[0]][self.target[1]]) * 10
		adyacentNode["f"] = adyacentNode["g"] + adyacentNode["h"]
		self.completeMap[adyacent["x"]][adyacent["y"]] = adyacentNode
		return adyacentNode


	def getPathResult(self, targetNode):
		pathList = []
		finalized = False
		lastNode = targetNode
		while (not finalized):
			pathList.append(lastNode)
			if lastNode["dad"] != None:
				lastNode = lastNode["dad"]
			else:
				finalized = True
		pathList.reverse()
		return pathList


	def printResultPath(self, pathList):
		caminoResultante = "==>Camino Resultante: "
		for i in range(len(pathList)):
			caminoResultante = caminoResultante + "(" + str(pathList[i]["x"]) + "," + str(pathList[i]["y"]) + ")"
		print(caminoResultante)


	def findPath(self):
		openList = [self.completeMap[self.init[0]][self.init[1]]]
		closedList = []
		pathResult = []
		end = False
		while not end:
			node = openList[0]
			closedList.append(node)
			openList.pop(0)
			neighbours = self.getNeighbours(node)
			# self.printNeighbours(node, neighbours)
			j = 0
			while (not end and j < len(neighbours)):
				adyacent = self.completeMap[neighbours[j]["x"]][neighbours[j]["y"]] 
				if self.arrivedToTarget(adyacent, self.target):
					end = True
					self.completeMap[adyacent["x"]][adyacent["y"]]["dad"] = node
					adyacent = self.completeMap[adyacent["x"]][adyacent["y"]]
					pathResult = self.getPathResult(adyacent)
				else:
					existsInClosedList = next((item for item in closedList if item["x"] == adyacent["x"] and item["y"] == adyacent["y"]), False)
					if not existsInClosedList:
						newG = self.calculateG(node, adyacent)
						existsInOpenList = next((item for item in openList if item["x"] == adyacent["x"] and item["y"] == adyacent["y"]), False)
						if existsInOpenList:
							if newG < adyacent["g"] :
								adyacent = self.setParentAndRecalculateFactors(node, adyacent, newG)
						else:
							adyacent = self.setParentAndRecalculateFactors(node, adyacent, newG)
							openList.append(adyacent)
				j = j + 1
			openList = sorted(openList, key=lambda node: node["f"])
		self.pathResult = pathResult
		return pathResult