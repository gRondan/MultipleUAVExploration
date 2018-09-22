from stateMachine.statesEnum import ACTUALIZAR_MAPA
from algoritmo_aster import Pathfinder


class POICritico():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = ACTUALIZAR_MAPA
        self.bebop = bebop
        self.position_poi = dataBuffer
        self.messages = messages

    def getNextState(self):
        return self.nextState

    def execute(self):
        initialPosition = self.bebop.current_position
        finalPosition = self.position_poi
        pathfinder = Pathfinder(initialPosition, finalPosition)
        pathToFollow = pathfinder.findPath()
        pathfinder.printFinalMap()
        self.bebop.moveToPoiCritico(pathfinder.parsePathToCoordinates(pathToFollow))
        return self.position_poi

    def handleMessage(self, message):
        self.messages.append(message)
