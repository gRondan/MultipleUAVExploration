from stateMachine.statesEnum import ENVIAR_MENSAJES

class actualizarMapa():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = ENVIAR_MENSAJES
        self.bebop = bebop
        self.dataBuffer = dataBuffer
        self.previousState = previousState
        self.messages = messages

    def getNextState(self):
        return self.nextState

    def execute(self):
        self.bebop.updateSearchMap(self.bebop.current_position)
        return dataBuffer

    def handleMessage(self, message):
        self.messages.append(message)
