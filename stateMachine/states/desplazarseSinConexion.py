from stateMachine.statesEnum import ACTUALIZAR_MAPA_SIN_CONEXION, ATERRIZAR


class desplazarseSinConexion():
    def __init__(self, bebop, dataBuffer, previousState, message):
        self.previousState = previousState
        self.bebop = bebop
        self.client = dataBuffer

    def getNextState(self):
        if self.bebop.home == self.bebop.current_position:
            return ATERRIZAR
        else:
            return ACTUALIZAR_MAPA_SIN_CONEXION

    def execute(self):
        newPosition = self.bebop.explore(True)
        self.bebop.move(newPosition)
        return self.client
