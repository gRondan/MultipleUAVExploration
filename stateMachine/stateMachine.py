from stateMachine.statesEnum import (INICIO, DESPEGAR,
ASIGNAR_POI, BATERIA_BAJA, BATERIA_CRITICA, DESPLAZARSE, ACTUALIZAR_MAPA,
ENVIAR_MENSAJES, POI_VIGILAR, CARGAR, GENERAL, CHEQUEAR_STATUS_MISION,
ATERRIZAR, MISION_FINALIZADA, PING_SIN_CONEXION, CANCELAR_MISION,
ACTUALIZAR_MAPA_SIN_CONEXION, FIN, POI_CRITICO, DESPLAZARSE_SIN_CONEXION)
from stateMachine.states import (actualizarMapaSinConexion, actualizarMapa,
asignarPOI, aterrizar, bateriaBaja, bateriaCritica, cancelarMision, chequearStatus,
despegar, desplazarse, enviarMensajes, explorar, fin, inicio, misionFinalizada, POICritico,
POIVigilar, pingSinConexion, cargarBateria, desplazarseSinConexion)
from properties import TIMEOUT, TIME_BETWEEN_POI_PING
from flightplans import drone, droneTest
import stateMachine.statesEnum as enum
import time
from threading import Timer


class stateMachine():
    def __init__(self, home, initPoiPosition, POIPositions):
        self.initPoiPosition = initPoiPosition
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
        self.messages = {i: [] for i in dir(enum) if not i.startswith('_')}
        self.timerDrones = {}
        self.POIPositions = POIPositions

    def execute(self):
        endExecutionTimer = Timer(TIMEOUT, self.isEndMision)
        endExecutionTimer.start()
        while not self.end:
            print("currentState: " + str(self.currentState))
            if self.currentState == INICIO:
                self.state = inicio(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])
                # inicioState.execute()
                # currentState = inicioState.getNextState()
            elif self.currentState == DESPEGAR:
                self.client = self.dataBuffer
                self.dataBuffer = self.initPoiPosition
                self.state = despegar(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])
                # currentState = despegarState.getNextState()
            elif self.currentState == CANCELAR_MISION:
                self.state = cancelarMision()
                self.state = explorar(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])
                # previousState = currentState;
                # currentState = explorarState.getNextState()
            elif self.currentState == ASIGNAR_POI:
                self.state = asignarPOI(self.bebop, self.dataBuffer, self.previousState, self.client, self.messages[self.currentState])
                startTime = time.time()
                startTime.start()
                self.timerDrones[self.dataBuffer] = startTime
                # currentState = asignarPOIState.getNextState()
            elif self.currentState == BATERIA_BAJA:
                self.state = bateriaBaja(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = bateriaBajaState.getNextState()
            elif self.currentState == BATERIA_CRITICA:
                self.state = bateriaCritica(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = bateriaCriticaState.getNextState()
            elif self.currentState == DESPLAZARSE:
                self.state = desplazarse(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])
                # desplazarseState.execute()
                # currentState = desplazarseState.getNextState()
            elif self.currentState == ACTUALIZAR_MAPA:
                self.state = actualizarMapa(self.bebop, self.dataBuffer, self.previousState, self.timerDrones, self.messages[self.currentState])

                # currentState = actualizarMapaState.getNextState()
            elif self.currentState == ENVIAR_MENSAJES:
                self.state = enviarMensajes(self.bebop, self.dataBuffer, self.client, self.timerDrones, self.endMision, self.POIPositions, self.messages[self.currentState])

                # currentState = enviarMensajesState.getNextState()
            elif self.currentState == POI_VIGILAR:
                self.state = POIVigilar(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = POIVigilarState.getNextState()
            elif self.currentState == POI_CRITICO:
                self.state = POICritico(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = POICriticoState.getNextState()
            elif self.currentState == CHEQUEAR_STATUS_MISION:
                self.state = chequearStatus(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])
                self.chequearMision = False
                t = Timer(TIME_BETWEEN_POI_PING, self.isChequearMision)
                t.start()

                # currentState = chequearStatusState.getNextState()
            elif self.currentState == ATERRIZAR:
                self.state = aterrizar(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

            elif self.currentState == MISION_FINALIZADA:
                self.state = misionFinalizada(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = misionFinalizadaState.getNextState()
            elif self.currentState == CANCELAR_MISION:
                self.state = cancelarMision(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = cancelarMisionState.getNextState()
            elif self.currentState == PING_SIN_CONEXION:
                self.state = pingSinConexion(self.bebop, self.dataBuffer, self.previousState, self.client, self.messages[self.currentState])

                # currentState = sinConexionState.getNextState()
            elif self.currentState == FIN:
                self.state = cargarBateria(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

            elif self.currentState == ACTUALIZAR_MAPA_SIN_CONEXION:
                self.state = actualizarMapaSinConexion(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

            elif self.currentState == DESPLAZARSE_SIN_CONEXION:
                self.state = desplazarseSinConexion(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

            elif self.currentState == CARGAR:
                self.state = fin(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])
                self.end = True

            self.processState()

    def processState(self):
        self.dataBuffer = self.state.execute()
        self.messages[self.currentState] = []
        self.previousState = self.currentState
        self.currentState = self.state.getNextState()

    def isEndMision(self):
        self.endMision = True

    # server related methods
    def handleMessage(self, message):
        if message["state"] == GENERAL:
            if message["message_type"] == 'update_map':
                self.bebop.updateSearchMap(message["content"])
        elif self.currentState == message["state"]:
            self.state.handleMessage(message)
        else:
            self.messages[message["state"]].append(message)
