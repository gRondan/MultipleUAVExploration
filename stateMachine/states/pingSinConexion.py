from stateMachine.statesEnum import ATERRIZAR, CANCELAR_MISION, DESPLAZARSE_SIN_CONEXION, BATERIA_CRITICA, BATERIA_BAJA
from batteryEnum import LOW, CRITICAL


class pingSinConexion():
    def __init__(self, bebop, dataBuffer, previousState, client, message):
        self.bebop = bebop
        self.previousState = previousState
        self.client = client
        cont = len(self.client.check_friends())
        self.isConnected = cont > 0
        self.message = message

    def getNextState(self):
        if not self.isConnected:
            return DESPLAZARSE_SIN_CONEXION
        else:
            if self.bebop.poi_position is not None:
                return CANCELAR_MISION
            elif self.bebop.current_position == self.bebop.home:
                return ATERRIZAR
            elif self.bebop.checkBatteryStatus() == CRITICAL:
                return BATERIA_CRITICA
            elif self.bebop.checkBatteryStatus() == LOW:
                return BATERIA_BAJA

    def execute(self):
        return self.client

    def handleMessage(self, message):
        self.messages.append(message)
