from flightplans import drone

class fin():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.bebop = Bebop
        self.messages = messages

    def execute(self):
        self.bebop.disconnect()
        return None;

    def getNextState(self):
        return None;

    def handleMessage(self, message):
        self.messages.append(message)
