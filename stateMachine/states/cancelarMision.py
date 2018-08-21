class cancelarMision():
    def __init__(self):

    def getNextState():

        if cancelarMisionTransitions.isBateriaBaja():
            actualState = BATERIA_BAJA
        elif cancelarMisionTransitions.isBateriaCritica():
            actualState = BATERIA_CRITICA
        elif cancelarMisionTransitions.isExplorar():
            actualState = EXPLORAR
