from stateMachine.statesEnum import INICIO, DESPEGAR, EXPLORAR, ASIGNAR_POI, BATERIA_BAJA, BATERIA_CRITICA, DESPLAZARSE,
ACTUALIZAR_MAPA, ENVIAR_MENSAJES, POI_VIGILAR, POI_CRITICO,
CHEQUEAR_STATUS_MISION, ATERRIZAR, MISION_FINALIZADA, SIN_CONEXION, CANCELAR_MISION, FIN
from stateMachine.states import actualizarMapa, asignarPOI, aterrizar, bateriaBaja, bateriaCritica,
cancelarMision, chequearStatus, despegar, desplazarse, enviarMensajes, explorar, fin, inicio,
misionFinalizada, POICritico, POIVigilar, sinConexion
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


    def execute(self):
        while !self.end:
            print("currentState: "+str(self.currentState))
            if self.currentState == INICIO:
                self.state = inicio(self.bebop, self.dataBuffer, self.previousState)
                # inicioState.execute()
                # currentState = inicioState.getNextState()
            elif currentState == DESPEGAR:
                self.dataBuffer = self.isInitPOICritico or self.isInitPOIVigilar
                self.state = despegar(self.bebop, self.dataBuffer, self.previousState)
                # despegarState.execute()
                # currentState = despegarState.getNextState()

            elif currentState == EXPLORAR:
                self.state = explorar()
                # previousState = currentState;
                # currentState = explorarState.getNextState()
            elif currentState == ASIGNAR_POI:
                self.state = asignarPOI()

                # currentState = asignarPOIState.getNextState()
            elif currentState == BATERIA_BAJA:
                self.state = bateriaBaja()

                # currentState = bateriaBajaState.getNextState()
            elif currentState == BATERIA_CRITICA:
                self.state = bateriaCritica()

                # currentState = bateriaCriticaState.getNextState()
            elif currentState == DESPLAZARSE:
                self.state = desplazarse(bebop, previousState)
                # desplazarseState.execute()
                # currentState = desplazarseState.getNextState()
            elif currentState == ACTUALIZAR_MAPA:
                self.state = actualizarMapa()

                # currentState = actualizarMapaState.getNextState()
            elif currentState == ENVIAR_MENSAJES:
                self.state = enviarMensajes()

                # currentState = enviarMensajesState.getNextState()
            elif currentState == POI_VIGILAR:
                self.state = POIVigilar()

                # currentState = POIVigilarState.getNextState()
            elif currentState == POI_CRITICO:
                self.state = POICritico()

                # currentState = POICriticoState.getNextState()
            elif currentState == CHEQUEAR_STATUS_MISION:
                self.state = chequearStatus()

                # currentState = chequearStatusState.getNextState()
            elif currentState == ATERRIZAR:
                self.state = aterrizar()

                # currentState = aterrizarState.getNextState()
            elif currentState == MISION_FINALIZADA:
                self.state = misionFinalizada()

                # currentState = misionFinalizadaState.getNextState()
            elif currentState == CANCELAR_MISION:
                self.state = cancelarMision()

                # currentState = cancelarMisionState.getNextState()
            elif currentState == SIN_CONEXION:
                self.state = sinConexion()

                # currentState = sinConexionState.getNextState()
            elif currentState == FIN:
                self.state = fin(self.bebop, self.dataBuffer, self.previousState)
                self.end = True
            self.processState()

    def processState(self):
        self.dataBuffer = self.state.execute()
        self.previousState = self.currentState
        self.currentState = self.state.getNextState()
