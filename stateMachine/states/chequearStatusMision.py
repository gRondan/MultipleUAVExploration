from connections import client
from connections.message_type import MISSION_OK
from stateMachine.statesEnum import ASIGNAR_POI, POI_CRITICO
from utils import createMessage, convertStringToTuple, getClosestPOI
from properties import TIME_BETWEEN_POI_PING
import threading


class chequearStatusMision():
    def __init__(self, bebop, dataBuffer, previousState, client, checkMissionStatus, poisVigilar, assignedPOIs, messages):
        self.messages = messages
        self.client = client
        self.nextState = dataBuffer
        self.poisVigilar = poisVigilar
        self.assignedPOIs = assignedPOIs
        self.checkMissionStatus = checkMissionStatus

    def getNextState(self):
        return self.nextState

    def execute(self):
        result = []
        for key in self.poisVigilar:
            if client.check_connection(self.assignedPOIs[key]["ip"]) == 0:
                client.send_message(createMessage(ASIGNAR_POI, MISSION_OK, key))
                self.poisVigilar.remove(key)
                timer2 = threading.Timer(TIME_BETWEEN_POI_PING, self.checkMissionStatus, (convertStringToTuple(key),))
                timer2.start()
            else:
                self.nextState = ASIGNAR_POI
                result.append(convertStringToTuple(key))
        minPoi = getClosestPOI(self.bebop.current_position, result)
        if minPoi is None:
            return None
        return {"poi": minPoi, "type": POI_CRITICO}

    def handleMessage(self, message):
        self.messages.append(message)
