from stateMachine.statesEnum import ENVIAR_MENSAJES, DESPLAZARSE

class POIVigilar():
	 def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = DESPLAZARSE
        self.bebop = bebop
        self.poi_position = dataBuffer
        self.previousState = previousState

    def getNextState():
        return self.nextState

    def execute(self):
        return self.bebop.explore(self.poi_position)
