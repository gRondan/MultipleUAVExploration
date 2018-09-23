from stateMachine.statesEnum import CHEQUEAR_STATUS_MISION, DESPLAZARSE_SIN_CONEXION, MISION_FINALIZADA, GENERAL, BATERIA_BAJA, BATERIA_CRITICA, POI_CRITICO, POI_VIGILAR, ASIGNAR_POI
from batteryEnum import LOW, NORMAL
from utils import createMessage, getClosestPOI, convertStringToTuple
from connections.message_type import UPDATE_MAP
import utils
from properties import POI_POSITIONS


class enviarMensajes():
    def __init__(self, bebop, dataBuffer, client, assignedPOIs, timeout, isAlone, poisVigilar, poisCritico, messages):
        self.bebop = bebop
        self.nextState = dataBuffer
        self.client = client
        self.assignedPOIs = assignedPOIs
        self.timeout = timeout
        self.POIPositions = POI_POSITIONS
        self.isAlone = isAlone
        self.poisVigilar = poisVigilar
        self.poisCritico = poisCritico

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
            if self.bebop.poi_position is not None:
                if self.bebop.poi_position in self.poisCritico:
                    self.nextState = POI_CRITICO
                else:
                    self.nextState = POI_VIGILAR
                return self.bebop.poi_position
            isChequearMisionResult = self.isChequearMision()
            if isChequearMisionResult is not None:
                return isChequearMisionResult
            else:
                return self.isAsignarPOI()
        return None

#       si para algun POI ya asignado se cumple que salto su timer de chequee voy al estado chequearStatusMision
    def isChequearMision(self):
        if not self.isAlone:
            for key in self.assignedPOIs:
                poi = convertStringToTuple(key)
                if (poi in self.poisVigilar) or (poi in self.poisCritico):
                    checkStatusNextState = self.nextState
                    self.nextState = CHEQUEAR_STATUS_MISION
                    return checkStatusNextState
        return None

    def isAsignarPOI(self):
        result = None
        if len(self.poisCritico) > 0:
            minPoi = getClosestPOI(self.bebop.current_position, self.poisCritico)
            if minPoi is None:
                return None
            self.poisCritico.remove(minPoi)
            self.nextState = ASIGNAR_POI
            result = {"poi": minPoi, "type": POI_CRITICO}
        elif len(self.poisVigilar) > 0:
            minPoi = getClosestPOI(self.bebop.current_position, self.poisVigilar)
            if minPoi is None:
                return self.bebop.poi_position
            self.poisVigilar.remove(minPoi)
            result = {"poi": minPoi, "type": POI_VIGILAR}
            self.nextState = ASIGNAR_POI
        return result

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
