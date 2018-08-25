from stateMachine.states import DESPLAZARSE

class explorar():
    def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = DESPLAZARSE
        self.bebop = bebop
        self.dataBuffer = dataBuffer

    def getNextState():
        return self.nextState

    def execute():
        return self.bebop.explorar()
