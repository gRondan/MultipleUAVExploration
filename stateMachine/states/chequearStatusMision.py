from connections import client
from connections.message_type import MISSION_OK
from stateMachine.statesEnum import ASIGNAR_POI, GENERAL
from utils import createMessage
import time

class chequearStatusMision():
    def __init__(self, bebop, dataBuffer, previousState, client, timerChequearStatus, messages):
        self.ip = dataBuffer["ip"]
        self.messages = messages
        self.client = client
        self.nextState = dataBuffer["state"]
        self.timerChequearStatus = timerChequearStatus

    def getNextState(self):
        return self.nextState

    def execute(self):
        result = None
        if client.check_connection(self.ip) == 0
            client.send_message(createMessage(ASIGNAR_POI,MISSION_OK,"ok"))
        else
            self.nextState = ASIGNAR_POI
            result = self.ip
        self.timerChequearStatus[self.ip] = time.time()
        return result

    def handleMessage(self, message):
        self.messages.append(message)
