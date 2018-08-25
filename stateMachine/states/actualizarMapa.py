from stateMachine.statesEnum import ENVIAR_MENSAJES

class actualizarMapa():
    def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = ENVIAR_MENSAJES
        self.bebop = bebop
        self.dataBuffer = dataBuffer
        self.previousState = previousState

    def getNextState():
        return self.nextState

    def execute():
        self.bebop.updateSearchMap(self.bebop.current_position)
        return dataBuffer
