class bateriaBaja():
    def __init__(self, messages):
        self.nextState = DESPLAZARSE
        self.messages = messages
    def getNextState():
        return self.nextState
    def handleMessage(self, message):
        self.messages.append(message)
