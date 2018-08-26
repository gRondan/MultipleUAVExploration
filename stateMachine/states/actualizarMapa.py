from stateMachine.statesEnum import ENVIAR_MENSAJES
from threading import Timer
from properties import POI_TIMERS, POI_POSITIONS


class actualizarMapa():
    def __init__(self, bebop, dataBuffer, previousState, timerPOIs, timeoutPoi, messages):
        self.nextState = ENVIAR_MENSAJES
        self.bebop = bebop
        self.previousState = previousState
        self.timerPOIs = timerPOIs
        self.messages = messages
        self.dataBuffer = dataBuffer
        self.timeoutPoi = timeoutPoi

    def getNextState(self):
        return self.nextState

    def execute(self):
        current_position = self.bebop.current_position
        if (self.bebop.poi_position == current_position):
            timeout = POI_TIMERS[POI_POSITIONS.index(current_position)]
            executionTimer = Timer(timeout, self.isEndMision)
            executionTimer.start()
            self.timerPOIs.remove(current_position)
        self.bebop.updateSearchMap(self.bebop.current_position)
        return self.dataBuffer

    def handleMessage(self, message):
        self.messages.append(message)
