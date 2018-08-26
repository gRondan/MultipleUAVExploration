from utils import createMessage
from stateMachine.statesEnum import FIN
from connections.message_type import END_MISSION

class fin():
    def __init__(self, bebop, dataBuffer, previousState, client, messages):
        self.bebop = bebop
        self.messages = messages
        self.client = client

    def execute(self):
        self.bebop.disconnect()
        self.client.send_direct_message(self.bebop.ip, createMessage(FIN, END_MISSION, "end"))
        return None

    def getNextState(self):
        return None

    def handleMessage(self, message):
        self.messages.append(message)
