from stateMachine.statesEnum import CHEQUEAR_STATUS_MISION, DESPLAZARSE_SIN_CONEXION, MISION_FINALIZADA, GENERAL, BATERIA_BAJA, BATERIA_CRITICA
from batteryEnum import CRITICAL, LOW, NORMAL
from utils import createMessage
from connections.message_type import UPDATE_MAP
from properties import TIME_BETWEEN_POI_PING, POI_EPSILON
import time
import utils


class enviarMensajes():
    def __init__(self, bebop, dataBuffer, client, timerChequearStatus, timeout, POIPositions, isAlone, messages):
        self.bebop = bebop
        self.nextState = dataBuffer
        self.client = client
        self.timerChequearStatus = timerChequearStatus
        self.timeout = timeout
        self.POIPositions = POIPositions
        self.isAlone = isAlone

    def getNextState(self):
        nextState = None
        if self.timeout:
            nextState = MISION_FINALIZADA
        else:
            nextState = self.checkBatteryStatus()
        return nextState

    def execute(self):
        if not self.timeout:
            if len(self.client.check_friends()) != 0:
                self.client.send_message(createMessage(GENERAL, UPDATE_MAP, utils.convertTupleToString(self.bebop.current_position)))
            elif not self.isAlone:
                self.nextState = DESPLAZARSE_SIN_CONEXION
                return self.client
            poi = self.isAsignarPOI()
            if poi is not None:
                return self.isChequearMision()
            return poi
        return None

    def isChequearMision(self):
        if not self.isAlone:
            for key, value in self.timerChequearStatus.items():
                if ((time.time() - value) > TIME_BETWEEN_POI_PING):
                    self.nextState = CHEQUEAR_STATUS_MISION
                    return dict({"ip": key, "state": self.nextState})
        return None

    def isAsignarPOI(self):
        for poi in self.POIPositions:
            if time.time() - self.bebop.search_map[poi[0]][poi[1]] > POI_EPSILON:
                return poi
        return None

    def handleMessage(self, message):
        self.messages.append(message)

    def checkBatteryStatus(self):
        batteryStatus = self.bebop.checkBatteryStatus()
        if batteryStatus == NORMAL:
            return self.nextState
        elif batteryStatus == LOW:
            return BATERIA_BAJA
        else:
            return BATERIA_CRITICA
