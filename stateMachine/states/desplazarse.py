from stateMachine.statesEnum import BATERIA_BAJA, BATERIA_CRITICA, ATERRIZAR, ACTUALIZAR_MAPA

class desplazarse():
    def __init__(self, previousState, bebop, new_position):
        self.previousState = previousState
        self.bebop = bebop
        self.new_position = new_position

    def getNextState():
        if (self.previousState == BATERIA_BAJA or self.previousState == BATERIA_CRITICA) and self.bebop.home == self.bebop.current_position:
            return ATERRIZAR
        elif desplazarseTrTransitions.isAterrizar():
            return ACTUALIZAR_MAPA

    def execute(self):
        self.bebop.move(self.new_position)
        return self.new_position
