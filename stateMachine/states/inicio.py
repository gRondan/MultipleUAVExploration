from stateMachine.statesEnum import DESPEGAR
from connections import server
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
        my_ip = server.get_server_ip()
        self.bebop.initialize(my_ip)
        client_handler = threading.Thread(
            target=server.run_server,
            args=(my_ip, self.bebop,)
        )
        client_handler.start()
        client1 = client.client()
        client1.search_friends(my_ip)
        return client1

    def handleMessage(self, message):
        self.messages.append(message)
