from flightplans import drone
from stateMachine.statesEnum import CHEQUEAR_STATUS_MISION, SIN_CONEXION, MISION_FINALIZADA

class enviarMensajes():
    def __init__(self, bebop, dataBuffer, client, chequearMision, timeout):
        self.bebop = bebop
        self.nextState = dataBuffer
        self.client = client
        self.chequearMision = chequearMision
        self.timeout = timeout

    def getNextState(self):
        nextState = None
        if self.timeout:
            nextState = MISION_FINALIZADA
        elif self.chequearMision:
            nextState = CHEQUEAR_STATUS_MISION
        else:
            nextState = self.nextState
        return nextState

    def execute(self):
        if not self.timeout:
            if len(client.check_friends()) > 0:
                message = bebop.current_position
                client.send_message(message)
            else:
                self.nextState = SIN_CONEXION
        return None
