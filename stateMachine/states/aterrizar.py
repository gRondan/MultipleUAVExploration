class aterrizar():
    def __init__(self, bebop, dataBuffer, previousState):
        self.bebop = bebop
        self.previousState = previousState
        self.dataBuffer = dataBuffer

    def getNextState():
        if self.previousState == DESPLAZARSE:
            return DESPEGAR
        return CARGAR

    def execute():
        self.bebop.land()