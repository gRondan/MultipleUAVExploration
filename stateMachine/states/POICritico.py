from stateMachine.statesEnum import ACTUALIZAR_MAPA

class POICritico():
    def __init__(self, bebop, dataBuffer, previousState, messages):
        self.nextState = ACTUALIZAR_MAPA
        self.bebop = bebop
        self.position_poi = dataBuffer
        self.messages = messages

    def getNextState():
        return self.nextState

    def execute(self):
        self.bebop.move(self.position_poi)
        return self.position_poi
  
    def handleMessage(self, message):
        self.messages.append(message)
