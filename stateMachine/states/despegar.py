from stateMachine.statesEnum import ASIGNAR_POI, EXPLORAR, BATERIA_BAJA, BATERIA_CRITICA, POI_CRITICO, POI_VIGILAR
from batteryEnum import LOW, CRITICAL
from properties import INIT_POI_POSITION, INIT_POI_POSITION_CRITICO


class despegar():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.poiCritico = INIT_POI_POSITION_CRITICO
        self.poiVigilar = INIT_POI_POSITION
        self.bebop = bebop
        self.isAsignarPOI = dataBuffer
        self.messages = messages

    def getNextState(self):
        nextState = None
        if self.poiVigilar is not None or self.poiCritico is not None:
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
        if self.poiVigilar is not None:
            return dict({"poi": self.poiVigilar, "type": POI_VIGILAR})
        elif self.poiCritico is not None:
            return dict({"poi": self.poiCritico, "type": POI_CRITICO})
        return None

    def handleMessage(self, message):
        self.messages.append(message)
