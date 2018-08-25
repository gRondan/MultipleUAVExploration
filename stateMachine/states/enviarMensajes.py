from flightplans import drone
from stateMachine.statesEnum import CHEQUEAR_STATUS_MISION, SIN_CONEXION, MISION_FINALIZADA
from utils import createMessage
from properties import TIME_BETWEEN_POI_PING

class enviarMensajes():
    def __init__(self, bebop, dataBuffer, client, timerChequearStatus, timeout):
        self.bebop = bebop
        self.nextState = dataBuffer
        self.client = client
        self.timerChequearStatus = timerChequearStatus
        self.timeout = timeout

    def getNextState(self):
        nextState = None
        if self.timeout:
            nextState = MISION_FINALIZADA
        else:
            nextState = self.nextState
        return nextState

    def execute(self):
        if not self.timeout:
            if len(client.check_friends()) != 0:
                client.send_message(createMessage(ENVIAR_MENSAJES,UPDATE_MAP,utils.convertTupleToString(bebop.current_position)))
            else:
                self.nextState = SIN_CONEXION
        return isChequearMision()

    def isChequearMision(self):
        for key, value in self.timerChequearStatus.items():
            if ((time.time() - value) > TIME_BETWEEN_POI_PING):
                self.nextState = CHEQUEAR_STATUS_MISION
                return dict({"ip":key,"state":self.nextState})
        return None
