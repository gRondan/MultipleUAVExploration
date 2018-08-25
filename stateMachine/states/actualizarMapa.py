from stateMachine.statesEnum import ENVIAR_MENSAJES

class actualizarMapa():
    def __init__(self, bebop, dataBuffer, previousState,timerDrones):
        self.nextState = ENVIAR_MENSAJES
        self.bebop = bebop
        self.timerDrones = timerDrones
        self.previousState = previousState
        self.dataBuffer = dataBuffer

    def getNextState(self):
        return self.nextState

    def execute(self):
        self.bebop.updateSearchMap(self.bebop.current_position)
        if (self.bebop.poi_position == self.bebop.home):
            del self.timerDrones[self.bebop.ip]
        return self.dataBuffer
