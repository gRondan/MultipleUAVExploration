from stateMachine.statesEnum import DESPLAZARSE_SIN_CONEXION, FIN, CARGAR


class aterrizar():
    def __init__(self, bebop, dataBuffer, previousState, timeout, messages):
        self.bebop = bebop
        self.previousState = previousState
        self.dataBuffer = dataBuffer
        self.messages = messages
        self.timeout = timeout

    def getNextState(self):
        if self.previousState == DESPLAZARSE_SIN_CONEXION or self.timeout:
            return FIN
        return CARGAR

    def execute(self):
        self.bebop.land()

    def handleMessage(self, message):
        self.messages.append(message)
