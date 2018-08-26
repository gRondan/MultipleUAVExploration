from stateMachine.statesEnum import BATERIA_BAJA, BATERIA_CRITICA, ATERRIZAR, ACTUALIZAR_MAPA


class desplazarse():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.previousState = previousState
        self.bebop = bebop
        self.new_position = dataBuffer
        self.messages = messages

    def getNextState(self):
        if (self.previousState == BATERIA_BAJA or self.previousState == BATERIA_CRITICA) and self.bebop.home == self.bebop.current_position:
            return ATERRIZAR
        else:
            return ACTUALIZAR_MAPA

    def execute(self):
        self.bebop.move(self.new_position)
        return self.previousState

    def handleMessage(self, message):
        self.messages.append(message)
