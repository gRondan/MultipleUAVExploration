from stateMachine.states import DESPLAZARSE

class explorar():
    def __init__(self, bebop):
        self.nextState = DESPLAZARSE
        self.bebop = bebop

    def getNextState():
        return self.nextState

    def execute():
        return self.bebop.explorar()
