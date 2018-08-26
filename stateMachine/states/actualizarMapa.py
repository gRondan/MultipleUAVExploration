from stateMachine.statesEnum import ENVIAR_MENSAJES

class actualizarMapa():
    def __init__(self, bebop, dataBuffer, previousState,timerDrones, messages):
        self.nextState = ENVIAR_MENSAJES
        self.bebop = bebop
        self.timerDrones = timerDrones
        self.previousState = previousState
        self.messages = messages
        self.dataBuffer = dataBuffer

    def getNextState(self):
        return self.nextState

    def execute(self):
        if (self.bebop.poi_position == self.bebop.home):
            del self.timerDrones[self.bebop.ip]
        self.bebop.updateSearchMap(self.bebop.current_position)
        return self.dataBuffer
      
    def handleMessage(self, message):
        self.messages.append(message)
        
