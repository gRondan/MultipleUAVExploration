from stateMachine.statesEnum import ENVIAR_MENSAJES, EXPLORAR
from threading import Timer
from utils import convertTupleToString
from properties import POI_POSITIONS, POI_TIMERS


class actualizarMapa():
    def __init__(self, bebop, dataBuffer, previousState, poisVigilar, poiVigilarTimeout, poiVigilarTimeoutDict, messages):
        self.nextState = ENVIAR_MENSAJES
        self.bebop = bebop
        self.previousState = previousState
        self.messages = messages
        self.dataBuffer = dataBuffer
        self.poisVigilar = poisVigilar
        self.poiVigilarTimeout = poiVigilarTimeout
        self.poiVigilarTimeoutDict = poiVigilarTimeoutDict

    def getNextState(self):
        return self.nextState

    def execute(self):
        current_position = self.bebop.current_position
        nextState = self.dataBuffer
        print("ACTUALIZAR_MAPA", " self.bebop.poi_position ", self.bebop.poi_position, " current_position ", current_position)
        if (self.bebop.poi_position == current_position):
            self.bebop.poi_position = None
            poiKey = convertTupleToString(current_position)
            if (poiKey in self.poiVigilarTimeoutDict):
                executionTimer = self.poiVigilarTimeoutDict[poiKey]
                executionTimer.cancel()
                executionTimerNew = Timer(POI_TIMERS[POI_POSITIONS.index(current_position)], self.poiVigilarTimeout, (current_position, ))
                executionTimerNew.start()
                self.poiVigilarTimeoutDict[poiKey] = executionTimerNew
            if current_position in self.poisVigilar:
                self.poisVigilar.remove(current_position)
            nextState = EXPLORAR
        self.bebop.updateSearchMap(self.bebop.current_position)
        return nextState

    def handleMessage(self, message):
        self.messages.append(message)
