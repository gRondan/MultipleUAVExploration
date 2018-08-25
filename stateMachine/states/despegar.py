from stateMachine.statesEnum import ASIGNAR_POI, EXPLORAR, BATERIA_BAJA, BATERIA_CRITICA

class despegar():
    def __init__(self):

    def getNextState():
        if despegarTransitions.isAsignarPOI():
            actualState = ASIGNAR_POI
        elif despegarTransitions.isExplorar():
            actualState = EXPLORAR
        elif despegarTransitions.isBateriaBaja():
            actualState = BATERIA_BAJA
        elif despegarTransitions.isBateriaCritica():
            actualState = BATERIA_CRITICA

    def
