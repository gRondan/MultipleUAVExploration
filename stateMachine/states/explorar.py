from stateMachine.states import DESPLAZARSE

class explorar():
    def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = DESPLAZARSE
        self.bebop = bebop
        self.dataBuffer = dataBuffer

    def getNextState(self):
        return self.nextState

    def execute(self):
        return self.bebop.explore(None)
