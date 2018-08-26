class cancelarMision():
    def __init__(self, messages):
        self.messages = messages
    def getNextState():

        if cancelarMisionTransitions.isBateriaBaja():
            actualState = BATERIA_BAJA
        elif cancelarMisionTransitions.isBateriaCritica():
            actualState = BATERIA_CRITICA
        elif cancelarMisionTransitions.isExplorar():
            actualState = EXPLORAR
    def handleMessage(self, message):
        self.messages.append(message)
