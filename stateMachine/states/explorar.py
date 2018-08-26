from stateMachine.states import DESPLAZARSE

class explorar():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = DESPLAZARSE
        self.bebop = bebop
        self.dataBuffer = dataBuffer
        self.messages = messages

    def getNextState(self):
        return self.nextState

    def execute(self):
        return self.bebop.explore(None)

    def handleMessage(self, message):
        self.messages.append(message)
