from stateMachine.statesEnum import DESPEGAR, INICIO
from connections.client import client
from threading import Timer, Lock
from properties import SYNC_WAIT, POI_POSITIONS, POI_TIMERS, SPHINX_SIMULATION
from utils import createMessage, convertTupleToString
from connections.message_type import SYNC


class inicio():
    def __init__(self, bebop, home, previousState, setTimerFunc, poiVigilarTimeoutDict, messages):
        self.nextState = DESPEGAR
        self.bebop = bebop
        self.home = home
        self.messages = messages
        self.syncLock = Lock()
        self.syncLock.acquire()
        self.awoken = False
        self.setTimerFunc = setTimerFunc
        self.poiVigilarTimeoutDict = poiVigilarTimeoutDict

    def getNextState(self):
        return self.nextState

    def execute(self):
        client1 = client()
        timer = Timer(SYNC_WAIT, self.wakeUp)
        timer.start()
        self.syncLock.acquire()
        client1.search_friends(self.bebop.ip)
        if not self.awoken:
            message = createMessage(INICIO, SYNC, 'wake up!')
            client1.send_message(message)
        for i in range(len(POI_POSITIONS)):
            new_timer = Timer(POI_TIMERS[i], self.setTimerFunc, (POI_POSITIONS[i],))
            new_timer.start()
            self.poiVigilarTimeoutDict[convertTupleToString(POI_POSITIONS[i])] = new_timer

        return client1

    def handleMessage(self, message):
        if message["message_type"] == SYNC:
            self.syncLock.release()
            self.awoken = True

    def wakeUp(self):
        self.syncLock.release()
