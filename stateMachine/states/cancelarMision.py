from stateMachine.statesEnum import ASIGNAR_POI, CANCELAR_MISION
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
        self.client.send_message(createMessage(CANCELAR_MISION, MISSION_ABORTED, self.bebop.ip))
        return None

    def handleMessage(self, message):
        self.messages.append(message)
