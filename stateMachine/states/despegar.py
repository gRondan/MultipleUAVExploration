from stateMachine.statesEnum import ASIGNAR_POI, EXPLORAR, BATERIA_BAJA, BATERIA_CRITICA
from batteryEnum import LOW, CRITICAL


class despegar():

    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.poiPosition = dataBuffer
        self.bebop = bebop
        self.isAsignarPOI = dataBuffer
        self.messages = messages

    def getNextState(self):
        nextState = None
        if self.poiPosition is not None:
            nextState = ASIGNAR_POI
        elif self.bebop.checkBatteryStatus() == CRITICAL:
            nextState = BATERIA_CRITICA
        elif self.bebop.checkBatteryStatus() == LOW:
            nextState = BATERIA_BAJA
        else:
            nextState = EXPLORAR
        return nextState

    def execute(self):
        self.bebop.take_off()
        if self.poiPosition is not None:
            return self.poiPosition
        else:
            return None

    def handleMessage(self, message):
        self.messages.append(message)
