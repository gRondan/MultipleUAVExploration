from stateMachine.statesEnum import INICIO, DESPEGAR, EXPLORAR, ASIGNAR_POI, BATERIA_BAJA, BATERIA_CRITICA, DESPLAZARSE,
ACTUALIZAR_MAPA, ENVIAR_MENSAJES, POI_VIGILAR, POI_CRITICO, CARGAR
CHEQUEAR_STATUS_MISION, ATERRIZAR, MISION_FINALIZADA, SIN_CONEXION, CANCELAR_MISION, FIN
from stateMachine.states import actualizarMapa, asignarPOI, aterrizar, bateriaBaja, bateriaCritica,
cancelarMision, chequearStatus, despegar, desplazarse, enviarMensajes, explorar, fin, inicio,
misionFinalizada, POICritico, POIVigilar, sinConexion, cargarBateria
from properties import TIMEOUT, TIME_BETWEEN_POI_PING
from flightplans import drone, droneTest

class stateMachine():

    def __init__(self, isInitPOICritico,  isInitPOIVigilar, home):
        self.isInitPOICritico = isInitPOICritico
        self.isInitPOIVigilar = isInitPOIVigilar
        self.home = home
        self.dataBuffer = home
        self.state = None
        self.end = False
        self.currentState = INICIO
        self.previousState = None
        self.bebop = drone.drone()
        self.client = None
        self.endMision = False
        self.chequearMision = False


    def execute(self):
        endExecutionTimer = Timer(TIMEOUT, self.isEndMision)
        endExecutionTimer.start()
        while !self.end:
            print("currentState: "+str(self.currentState))
            if self.currentState == INICIO:
                self.state = inicio(self.bebop, self.dataBuffer, self.previousState)
                # inicioState.execute()
                # currentState = inicioState.getNextState()
            elif currentState == DESPEGAR:
                self.client = self.dataBuffer
                self.dataBuffer = self.isInitPOICritico or self.isInitPOIVigilar
                self.state = despegar(self.bebop, self.dataBuffer, self.previousState)
                # despegarState.execute()
                # currentState = despegarState.getNextState()
            elif currentState == CANCELAR_MISION:
                self.state = cancelarMision()
                self.state = explorar(self.bebop, self.dataBuffer, self.previousState)
                # previousState = currentState;
                # currentState = explorarState.getNextState()
            elif currentState == ASIGNAR_POI:
                self.state = asignarPOI(self.bebop, self.dataBuffer, self.previousState)

                # currentState = asignarPOIState.getNextState()
            elif currentState == BATERIA_BAJA:
                self.state = bateriaBaja(self.bebop, self.dataBuffer, self.previousState)

                # currentState = bateriaBajaState.getNextState()
            elif currentState == BATERIA_CRITICA:
                self.state = bateriaCritica(self.bebop, self.dataBuffer, self.previousState)

                # currentState = bateriaCriticaState.getNextState()
            elif currentState == DESPLAZARSE:
                self.state = desplazarse(self.bebop, self.dataBuffer, self.previousState)
                # desplazarseState.execute()
                # currentState = desplazarseState.getNextState()
            elif currentState == ACTUALIZAR_MAPA:
                self.state = actualizarMapa(self.bebop, self.dataBuffer, self.previousState)

                # currentState = actualizarMapaState.getNextState()
            elif currentState == ENVIAR_MENSAJES:
                self.state = enviarMensajes(self.bebop, self.dataBuffer, self.client, self.chequearMision, self.endMision)

                # currentState = enviarMensajesState.getNextState()
            elif currentState == POI_VIGILAR:
                self.state = POIVigilar(self.bebop, self.dataBuffer, self.previousState)

                # currentState = POIVigilarState.getNextState()
            elif currentState == POI_CRITICO:
                self.state = POICritico(self.bebop, self.dataBuffer, self.previousState)

                # currentState = POICriticoState.getNextState()
            elif currentState == CHEQUEAR_STATUS_MISION:
                self.state = chequearStatus(self.bebop, self.dataBuffer, self.previousState)
                self.chequearMision = False
                t = Timer(TIME_BETWEEN_POI_PING, self.isChequearMision)
                t.start()

                # currentState = chequearStatusState.getNextState()
            elif currentState == ATERRIZAR:
                self.state = aterrizar(self.bebop, self.dataBuffer, self.previousState)

                # currentState = aterrizarState.getNextState()
            elif currentState == MISION_FINALIZADA:
                self.state = misionFinalizada(self.bebop, self.dataBuffer, self.previousState)

                # currentState = misionFinalizadaState.getNextState()
            elif currentState == CANCELAR_MISION:
                self.state = cancelarMision(self.bebop, self.dataBuffer, self.previousState)

                # currentState = cancelarMisionState.getNextState()
            elif currentState == SIN_CONEXION:
                self.state = sinConexion(self.bebop, self.dataBuffer, self.previousState, self.client)

                # currentState = sinConexionState.getNextState()
            elif currentState == FIN:
                self.state = cargarBateria(self.bebop, self.dataBuffer, self.previousState)

            elif currentState == CARGAR:
                self.state = fin(self.bebop, self.dataBuffer, self.previousState)
                self.end = True

            self.processState()

    def processState(self):
        self.dataBuffer = self.state.execute()
        self.previousState = self.currentState
        self.currentState = self.state.getNextState()

    def isChequearMision():
        self.chequearMision = True

    def isEndMision():
        self.endMision = True
