from stateMachine.statesEnum import ENVIAR_MENSAJES, DESPLAZARSE

class bateriaBaja():
	 def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = DESPLAZARSE
        self.bebop = bebop
        self.previousState = previousState

    def getNextState():
        return self.nextState

    def execute(self):
    	self.bebop.setPoiPosition(None)
        return self.bebop.explore()
