from stateMachine.statesEnum import ENVIAR_MENSAJES, POI_CRITICO

class POICritico():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = ENVIAR_MENSAJES
        self.bebop = bebop
        self.position_poi = dataBuffer
        self.messages = messages

    def getNextState():
        return self.nextState

    def execute(self):
        self.bebop.move(self.position_poi)
        return POI_CRITICO

    def handleMessage(self, message):
        self.messages.append(message)
