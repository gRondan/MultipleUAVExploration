from stateMachine.statesEnum import ASIGNAR_POI, EXPLORAR, BATERIA_BAJA, BATERIA_CRITICA
from batteryEnum import LOW, CRITICAL, NORMAL
from flightplans import drone

class despegar():
    def __init__(self, bebop,isAsignarPOI, previousState):
        self.isAsignarPOI = isAsignarPOI
        self.bebop = bebop

    def getNextState(self):
        nextState = None
        if self.isAsignarPOI:
            nextState = ASIGNAR_POI
        elif self.bebop.checkBatteryStatus == LOW:
            nextState = BATERIA_CRITICA
        else:
            nextState = EXPLORAR
        return nextState

    def execute(self):
        bebop.take_off()
        return None
