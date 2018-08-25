from stateMachine.statesEnum import ACTUALIZAR_POI

class POICritico():
    def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = ACTUALIZAR_POI
        self.bebop = bebop
        self.position_poi = dataBuffer

    def getNextState():
        return self.nextState

    def execute(self):
        self.bebop.move(self.position_poi)
        return self.position_poi