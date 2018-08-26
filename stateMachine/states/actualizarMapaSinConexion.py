from stateMachine.statesEnum import PING_SIN_CONEXION, GENERAL
from utils import createMessage
from connections.message_type import UPDATE_MAP
import utils


class actualizarMapaSinConexion():
    def __init__(self, bebop, dataBuffer, previousState):
        self.nextState = PING_SIN_CONEXION
        self.bebop = bebop
        self.previousState = previousState
        self.client = dataBuffer

    def getNextState(self):
        return self.nextState

    def execute(self):
        self.bebop.updateSearchMap(self.bebop.current_position)
        self.client.send_message(createMessage(GENERAL, UPDATE_MAP, utils.convertTupleToString(self.bebop.current_position)))
        return None
