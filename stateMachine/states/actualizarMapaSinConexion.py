from stateMachine.statesEnum import PING_SIN_CONEXION, ACTUALIZAR_MAPA_SIN_CONEXION
from utils import createMessage
from connections import client
from connections.message_type import UPDATE_MAP

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
        self.client.send_message(createMessage(ACTUALIZAR_MAPA_SIN_CONEXION, UPDATE_MAP, utils.convertTupleToString(self.bebop.current_position)))
        return None
