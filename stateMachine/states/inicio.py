from stateMachine.statesEnum import DESPEGAR
from pyparrot.Bebop import Bebop
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
            args=(my_ip, drone1,)
        )
        client_handler.start()
        client = client.client()
        client.search_friends(my_ip)

    def handleMessage(self, message):
        self.messages.append(message)
