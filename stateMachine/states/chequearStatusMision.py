class chequearStatusMision():
    def __init__(self, messages):
        self.messages = messages
    def getNextState():

        if chequearStatusMisionTransitions.isAsignarPOI():
            actualState = ASIGNAR_POI
        elif chequearStatusMisionTransitions.isExplorar():
            actualState = EXPLORAR
        elif chequearStatusMisionTransitions.isBateriaBaja():
            actualState = BATERIA_BAJA
        elif chequearStatusMisionTransitions.isBateriaCritica():
            actualState = BATERIA_CRITICA

    def handleMessage(self, message):
        self.messages.append(message)
