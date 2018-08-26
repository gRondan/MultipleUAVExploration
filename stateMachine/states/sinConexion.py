from stateMachine.states import ATERRIZAR, CANCELAR_MISION

class sinConexion():
    def __init__(self, bebop, dataBuffer, previousState, client):
        self.bebop = bebop
        self.dataBuffer = dataBuffer
        self.previousState = previousState
        self.client = client

    def getNextState(self):
        if self.bebop.current_position == self.bebop.home:
            return ATERRIZAR
        return CANCELAR_MISION

    def execute(self):
        disconnected = True
        while self.bebop.current_position != self.bebop.home and disconnected:
            new_coordinate = self.bebop.getNewCoordinate()
            self.bebop.move(new_coordinate)
            cont = self.client.check_friends()
            if len(cont) > 0:
                disconnected = False
        return None
