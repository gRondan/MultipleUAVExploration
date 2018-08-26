from stateMachine.statesEnum import DESPLAZARSE, DESPEGAR, CARGAR

class aterrizar():
    def __init__(self, bebop, dataBuffer, messages, previousState):
        self.bebop = bebop
        self.previousState = previousState
        self.dataBuffer = dataBuffer
        self.messages = messages

    def getNextState(self):
        if self.previousState == DESPLAZARSE:
            return DESPEGAR
        return CARGAR

    def execute(self):
        self.bebop.land()

    def handleMessage(self, message):
        self.messages.append(message)
