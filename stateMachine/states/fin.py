from utils import createMessage
from stateMachine.statesEnum import FIN
from connections.message_type import END_MISSION


class fin():
    def __init__(self, bebop, dataBuffer, previousState, client, logStats, messages):
        self.bebop = bebop
        self.messages = messages
        self.client = client
        self.logStats = logStats

    def execute(self):
        self.bebop.disconnect()
        self.client.send_direct_message(createMessage(FIN, END_MISSION, "end"), self.bebop.ip)
        self.logStats.endExecution()
        return None

    def getNextState(self):
        return None

    def handleMessage(self, message):
        self.messages.append(message)
