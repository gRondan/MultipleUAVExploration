from stateMachine.statesEnum import DESPEGAR
from connections.client import client


class inicio():
    def __init__(self, bebop, home, previousState, messages):
        self.nextState = DESPEGAR
        self.bebop = bebop
        self.home = home
        self.messages = messages

    def getNextState(self):
        return self.nextState

    def execute(self):
        client1 = client()
        # client1.search_friends(self.bebop.ip)
        return client1

    def handleMessage(self, message):
        self.messages.append(message)
