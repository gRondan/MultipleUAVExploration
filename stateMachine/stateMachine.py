from stateMachine.statesEnum import INICIO, DESPEGAR, EXPLORAR, ASIGNAR_POI, BATERIA_BAJA, BATERIA_CRITICA, DESPLAZARSE,
ACTUALIZAR_MAPA, ENVIAR_MENSAJES, POI_VIGILAR, POI_CRITICO,
CHEQUEAR_STATUS_MISION, ATERRIZAR, MISION_FINALIZADA, SIN_CONEXION, CANCELAR_MISION, FIN
from stateMachine.states import actualizarMapa, asignarPOI, aterrizar, bateriaBaja, bateriaCritica,
cancelarMision, chequearStatus, despegar, desplazarse, enviarMensajes, explorar, fin, inicio,
misionFinalizada, POICritico, POIVigilar, sinConexion
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
                self.state = explorar()
                # previousState = currentState;
                # currentState = explorarState.getNextState()
            elif currentState == ASIGNAR_POI:
                print("currentState: "+str(currentState))
                self.state = asignarPOI()

                # currentState = asignarPOIState.getNextState()
            elif currentState == BATERIA_BAJA:
                print("currentState: "+str(currentState))
                self.state = bateriaBaja()

                # currentState = bateriaBajaState.getNextState()
            elif currentState == BATERIA_CRITICA:
                print("currentState: "+str(currentState))
                self.state = bateriaCritica()

                # currentState = bateriaCriticaState.getNextState()
            elif currentState == DESPLAZARSE:
                print("currentState: "+str(currentState))
                self.state = desplazarse(bebop, previousState)
                # desplazarseState.execute()
                # currentState = desplazarseState.getNextState()
            elif currentState == ACTUALIZAR_MAPA:
                print("currentState: "+str(currentState))
                self.state = actualizarMapa()

                # currentState = actualizarMapaState.getNextState()
            elif currentState == ENVIAR_MENSAJES:
                print("currentState: "+str(currentState))
                self.state = enviarMensajes()

                # currentState = enviarMensajesState.getNextState()
            elif currentState == POI_VIGILAR:
                print("currentState: "+str(currentState))
                self.state = POIVigilar()

                # currentState = POIVigilarState.getNextState()
            elif currentState == POI_CRITICO:
                print("currentState: "+str(currentState))
                self.state = POICritico()

                # currentState = POICriticoState.getNextState()
            elif currentState == CHEQUEAR_STATUS_MISION:
                print("currentState: "+str(currentState))
                self.state = chequearStatus()

                # currentState = chequearStatusState.getNextState()
            elif currentState == ATERRIZAR:
                print("currentState: "+str(currentState))
                self.state = aterrizar()

                # currentState = aterrizarState.getNextState()
            elif currentState == MISION_FINALIZADA:
                print("currentState: "+str(currentState))
                self.state = misionFinalizada()

                # currentState = misionFinalizadaState.getNextState()
            elif currentState == CANCELAR_MISION:
                print("currentState: "+str(currentState))
                self.state = cancelarMision()

                # currentState = cancelarMisionState.getNextState()
            elif currentState == SIN_CONEXION:
                print("currentState: "+str(currentState))
                self.state = sinConexion()

                # currentState = sinConexionState.getNextState()
            elif currentState == FIN:
                print("currentState: "+str(currentState))
                self.state = fin()
                self.end = True
            self.processState()

    def processState(self):
        self.dataBuffer = self.state.execute()
        self.previousState = self.currentState
        self.currentState = self.state.getNextState()
