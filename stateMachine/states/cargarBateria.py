class cargarBateria():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = DESPEGAR
        self.dataBuffer = dataBuffer
        self.previousState = previousState
        self.messages = messages

    def getNextState():
        return self.nextState

    def handleMessage(self, message):
        self.messages.append(message)
