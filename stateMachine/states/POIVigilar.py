from stateMachine.statesEnum import DESPLAZARSE


class POIVigilar():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = DESPLAZARSE
        self.bebop = bebop
        self.poi = dataBuffer
        self.previousState = previousState
        self.messages = messages

    def getNextState(self):
        return self.nextState

    def execute(self):
        return self.bebop.explore(None)

    def handleMessage(self, message):
        self.messages.append(message)
