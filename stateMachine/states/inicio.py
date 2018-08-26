from stateMachine.statesEnum import DESPEGAR
from connections import connections
from connections import client
import threading


class inicio():
    def __init__(self, bebop, home, previousState, messages):
        self.nextState = DESPEGAR
        self.bebop = bebop
        self.home = home
        self.messages = messages

    def getNextState(self):
        return self.nextState

    def execute(self):
        self.bebop.initialize(self.home)
        return self.processConections()

    def processConections(self):
        my_ip = connections.get_server_ip()
        client_handler = threading.Thread(
            target=connections.run_server,
            args=(my_ip, self.bebop,)
        )
        client_handler.start()
        client1 = client.client()
        client1.search_friends(my_ip)
        return client1

    def handleMessage(self, message):
        self.messages.append(message)
