from stateMachine.statesEnum import ATERRIZAR


class misionFinalizada():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = ATERRIZAR
        self.bebop = bebop
        self.messages = messages

    def getNextState(self):
        return self.nextState

    def execute(self):
        self.bebop.goHome()
        return None

    def handleMessage(self, message):
        self.messages.append(message)
