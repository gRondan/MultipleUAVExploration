from connections.message_type import MISSION_OK
from stateMachine.statesEnum import ASIGNAR_POI, POI_CRITICO
from utils import createMessage, getClosestPOI, convertTupleToString
from properties import TIME_BETWEEN_POI_PING
import threading


class chequearStatusMision():
    def __init__(self, bebop, dataBuffer, previousState, client, checkMissionStatus, poisVigilar, assignedPOIs, poisCritico, messages):
        self.messages = messages
        self.bebop = bebop
        self.client = client
        self.nextState = dataBuffer
        self.poisVigilar = poisVigilar
        self.poisCritico = poisCritico
        self.assignedPOIs = assignedPOIs
        self.checkMissionStatus = checkMissionStatus

    def getNextState(self):
        return self.nextState

    def execute(self):
        result = []
        for key in self.poisVigilar:
            if convertTupleToString(key) in self.assignedPOIs andself.client.check_connection(self.assignedPOIs[convertTupleToString(key)]["ip"]) == 0:
                self.client.send_message(createMessage(ASIGNAR_POI, MISSION_OK, key))
                self.poisVigilar.remove(key)
                timer2 = threading.Timer(TIME_BETWEEN_POI_PING, self.checkMissionStatus, (key,))
                timer2.start()
            else:
                self.nextState = ASIGNAR_POI
                result.append(key)
        for key in self.poisCritico:
            if convertTupleToString(key) in self.assignedPOIs and self.client.check_connection(self.assignedPOIs[convertTupleToString(key)]["ip"]) == 0:
                self.client.send_message(createMessage(ASIGNAR_POI, MISSION_OK, key))
                self.poisCritico.remove(key)
                timer2 = threading.Timer(TIME_BETWEEN_POI_PING, self.checkMissionStatus, (key,))
                timer2.start()
            else:
                self.nextState = ASIGNAR_POI
                result.append(key)
        minPoi = getClosestPOI(self.bebop.current_position, result)
        if minPoi is None:
            return None
        return {"poi": minPoi, "type": POI_CRITICO}

    def handleMessage(self, message):
        self.messages.append(message)
