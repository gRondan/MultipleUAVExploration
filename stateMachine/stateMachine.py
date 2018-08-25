from stateMachine.statesEnum import INICIO, DESPEGAR, EXPLORAR, ASIGNAR_POI, BATERIA_BAJA, BATERIA_CRITICA, DESPLAZARSE,
ACTUALIZAR_MAPA, ENVIAR_MENSAJES, POI_VIGILAR, POI_CRITICO, CARGAR
CHEQUEAR_STATUS_MISION, ATERRIZAR, MISION_FINALIZADA, SIN_CONEXION, CANCELAR_MISION, FIN
from stateMachine.states import actualizarMapa, asignarPOI, aterrizar, bateriaBaja, bateriaCritica,
cancelarMision, chequearStatus, despegar, desplazarse, enviarMensajes, explorar, fin, inicio,
misionFinalizada, POICritico, POIVigilar, sinConexion, cargarBateria
from pyparrot.Bebop import Bebop
from flightplans import drone, droneTest

class stateMachine():

    def __init__(self, isInitPOICritico,  isInitPOIVigilar):
        self.isInitPOICritico = isInitPOICritico
        self.isInitPOIVigilar = isInitPOIVigilar
        self.dataBuffer = None
        self.state = None
        self.end = False
        self.currentState = INICIO

    def execute(self):
        while !end:
            if self.currentState == INICIO:
                print("currentState: "+str(currentState))
                self.state = inicio(bebop, home)
                # inicioState.execute()
                # currentState = inicioState.getNextState()
            elif currentState == DESPEGAR:
                print("currentState: "+str(currentState))
                self.state = despegar()
                # despegarState.execute()
                # currentState = despegarState.getNextState()

            elif currentState == EXPLORAR:
                print("currentState: "+str(currentState))
                self.state = explorar(self.bebop, self.dataBuffer, self.previousState)
                # previousState = currentState;
                # currentState = explorarState.getNextState()
            elif currentState == ASIGNAR_POI:
                print("currentState: "+str(currentState))
                self.state = asignarPOI(self.bebop, self.dataBuffer, self.previousState)

                # currentState = asignarPOIState.getNextState()
            elif currentState == BATERIA_BAJA:
                print("currentState: "+str(currentState))
                self.state = bateriaBaja(self.bebop, self.dataBuffer, self.previousState)

                # currentState = bateriaBajaState.getNextState()
            elif currentState == BATERIA_CRITICA:
                print("currentState: "+str(currentState))
                self.state = bateriaCritica(self.bebop, self.dataBuffer, self.previousState)

                # currentState = bateriaCriticaState.getNextState()
            elif currentState == DESPLAZARSE:
                print("currentState: "+str(currentState))
                self.state = desplazarse(self.bebop, self.dataBuffer, self.previousState)
                # desplazarseState.execute()
                # currentState = desplazarseState.getNextState()
            elif currentState == ACTUALIZAR_MAPA:
                print("currentState: "+str(currentState))
                self.state = actualizarMapa(self.bebop, self.dataBuffer, self.previousState)

                # currentState = actualizarMapaState.getNextState()
            elif currentState == ENVIAR_MENSAJES:
                print("currentState: "+str(currentState))
                self.state = enviarMensajes(self.bebop, self.dataBuffer, self.previousState)

                # currentState = enviarMensajesState.getNextState()
            elif currentState == POI_VIGILAR:
                print("currentState: "+str(currentState))
                self.state = POIVigilar(self.bebop, self.dataBuffer, self.previousState)

                # currentState = POIVigilarState.getNextState()
            elif currentState == POI_CRITICO:
                print("currentState: "+str(currentState))
                self.state = POICritico(self.bebop, self.dataBuffer, self.previousState)

                # currentState = POICriticoState.getNextState()
            elif currentState == CHEQUEAR_STATUS_MISION:
                print("currentState: "+str(currentState))
                self.state = chequearStatus(self.bebop, self.dataBuffer, self.previousState)

                # currentState = chequearStatusState.getNextState()
            elif currentState == ATERRIZAR:
                print("currentState: "+str(currentState))
                self.state = aterrizar(self.bebop, self.dataBuffer, self.previousState)

                # currentState = aterrizarState.getNextState()
            elif currentState == MISION_FINALIZADA:
                print("currentState: "+str(currentState))
                self.state = misionFinalizada(self.bebop, self.dataBuffer, self.previousState)

                # currentState = misionFinalizadaState.getNextState()
            elif currentState == CANCELAR_MISION:
                print("currentState: "+str(currentState))
                self.state = cancelarMision(self.bebop, self.dataBuffer, self.previousState)

                # currentState = cancelarMisionState.getNextState()
            elif currentState == SIN_CONEXION:
                print("currentState: "+str(currentState))
                self.state = sinConexion()

                # currentState = sinConexionState.getNextState()
            elif currentState == FIN:
                print("currentState: "+str(currentState))
                self.state = cargarBateria(self.bebop, self.dataBuffer, self.previousState)

            elif currentState == CARGAR:
                print("currentState: "+str(currentState))
                self.state = fin(self.bebop, self.dataBuffer, self.previousState)
                self.end = True

            self.processState()

    def processState(self):
        self.dataBuffer = self.state.execute()
        self.previousState = self.currentState
        self.currentState = self.state.getNextState()
