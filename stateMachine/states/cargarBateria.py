from stateMachine.statesEnum import DESPEGAR
import time


class cargarBateria():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = DESPEGAR
        self.bebop = bebop
        self.previousState = previousState
        self.messages = messages

    def getNextState(self):
        return self.nextState

    def execute(self):
        time.sleep(10)
        return None

    def handleMessage(self, message):
        self.messages.append(message)
