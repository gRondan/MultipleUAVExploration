from stateMachine.statesEnum import DESPEGAR
import time

class cargarBateria():
    def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = DESPEGAR
        self.bebop = bebop
        self.previousState = previousState

    def getNextState():
        return self.nextState

    def execute(self):
    	time.sleep(10)
        return None