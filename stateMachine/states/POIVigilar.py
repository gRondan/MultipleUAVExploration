from stateMachine.statesEnum import ENVIAR_MENSAJES, DESPLAZARSE

class POIVigilar():
	 def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = DESPLAZARSE
        self.bebop = bebop
        self.poi_position = dataBuffer
        self.previousState = previousState
		self.messages = messages

    def getNextState():
        return self.nextState

    def execute(self):
        return self.bebop.explore(self.poi_position)

    def handleMessage(self, message):
        self.messages.append(message)
