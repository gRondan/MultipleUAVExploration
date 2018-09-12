from algoritmo_aster import Pathfinder

puntoInicial = (2,2)
puntoFinal = (9,7)
pathfinder = Pathfinder(puntoInicial, puntoFinal)
path = pathfinder.findPath()
pathfinder.printResultPath(path)
pathfinder.printFinalMap()