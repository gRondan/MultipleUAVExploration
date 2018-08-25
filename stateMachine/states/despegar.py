from stateMachine.statesEnum import ASIGNAR_POI, EXPLORAR, BATERIA_BAJA, BATERIA_CRITICA
from batteryEnum import LOW, CRITICAL, NORMAL
from flightplans import drone

class despegar():
    def __init__(self, bebop, dataBuffer, previousState):
        self.poiPosition = dataBuffer
        self.bebop = bebop

    def getNextState(self):
        nextState = None
        if self.poiPosition != None:
            nextState = ASIGNAR_POI
        elif self.bebop.checkBatteryStatus() == CRITICAL:
            nextState = BATERIA_CRITICA
        elif self.bebop.checkBatteryStatus() == LOW:
            nextState = BATERIA_BAJA
        else:
            nextState = EXPLORAR
        return nextState

    def execute(self):
        bebop.take_off()
        if self.poiPosition != None:
            return self.poiPosition
        else:
            return None
