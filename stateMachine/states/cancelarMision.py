from stateMachine.statesEnum import ASIGNAR_POI, GENERAL
from utils import createMessage
from connections.message_type import MISSION_ABORTED


class cancelarMision():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.bebop = bebop
        self.client = dataBuffer
        self.messages = messages

    def getNextState(self):
        return ASIGNAR_POI

    def execute(self):
        self.client.send_message(createMessage(GENERAL, MISSION_ABORTED, dict({"ip": self.bebop.ip, "poi": self.bebop.poi_position})))
        return None

    def handleMessage(self, message):
        self.messages.append(message)
