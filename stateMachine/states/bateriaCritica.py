from stateMachine.statesEnum import ATERRIZAR

class bateriaCritica():
    def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = ATERRIZAR
        self.bebop = bebop
        self.dataBuffer = dataBuffer

    def getNextState(self):
        return ATERRIZAR

    def execute(self):
        self.bebop.goHome()
        return None
