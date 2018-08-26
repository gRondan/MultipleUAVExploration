from stateMachine.statesEnum import ATERRIZAR

class bateriaCritica():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = ATERRIZAR
        self.bebop = bebop
        self.dataBuffer = dataBuffer
        self.messages = messages

    def getNextState(self):
        return ATERRIZAR

    def execute(self):
        self.bebop.goHome()
        return None

    def handleMessage(self, message):
        self.messages.append(message)
