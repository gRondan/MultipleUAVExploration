from stateMachine.statesEnum import ATERRIZAR

class misionFinalizada():
    def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = ATERRIZAR
        self.bebop = bebop

    def getNextState():
        return self.nextState
        
    def execute(self):
        self.bebop.goHome()
        return None
