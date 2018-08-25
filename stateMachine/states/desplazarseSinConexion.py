from stateMachine.statesEnum import ACTUALIZAR_MAPA_SIN_CONEXION, ATERRIZAR

class desplazarse():
    def __init__(self, bebop, dataBuffer, previousState):
        self.previousState = previousState
        self.bebop = bebop
        self.client = dataBuffer

    def getNextState(self):
        if self.bebop.home == self.bebop.current_position:
            return ATERRIZAR
        else:
            return ACTUALIZAR_MAPA_SIN_CONEXION

    def execute(self):
        newPosition = self.bebop.explore(self.bebop.home)
        self.bebop.move(newPosition)
        return self.client
