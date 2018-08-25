from stateMachine.statesEnum import DESPLAZARSE, DESPEGAR, CARGAR

class aterrizar():
    def __init__(self, bebop, dataBuffer, previousState):
        self.bebop = bebop
        self.previousState = previousState
        self.dataBuffer = dataBuffer

    def getNextState(self):
        if self.previousState == DESPLAZARSE:
            return DESPEGAR
        return CARGAR

    def execute(self):
        self.bebop.land()
