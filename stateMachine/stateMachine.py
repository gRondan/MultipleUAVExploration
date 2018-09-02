from stateMachine.statesEnum import (INICIO, DESPEGAR,
ASIGNAR_POI, BATERIA_BAJA, BATERIA_CRITICA, DESPLAZARSE, ACTUALIZAR_MAPA,
ENVIAR_MENSAJES, POI_VIGILAR, CARGAR, GENERAL, CHEQUEAR_STATUS_MISION,
ATERRIZAR, MISION_FINALIZADA, PING_SIN_CONEXION, CANCELAR_MISION,
ACTUALIZAR_MAPA_SIN_CONEXION, FIN, POI_CRITICO, DESPLAZARSE_SIN_CONEXION,
EXPLORAR)
from stateMachine.states import (actualizarMapaSinConexion, actualizarMapa,
asignarPOI, aterrizar, bateriaBaja, bateriaCritica, cancelarMision, chequearStatusMision,
despegar, desplazarse, enviarMensajes, explorar, fin, inicio, misionFinalizada, POICritico,
POIVigilar, pingSinConexion, cargarBateria, desplazarseSinConexion)
from properties import TIMEOUT
from utils import createMessage
from connections.message_type import UPDATE_MAP, MISSION_ABORTED, POI_ALREADY_ASSIGNED
import stateMachine.statesEnum as enum
from threading import Timer, Lock


class stateMachine():
    def __init__(self, home, initPoiPosition, isAlone, bebop):
        self.initPoiPosition = initPoiPosition
        self.home = home
        self.dataBuffer = home
        self.state = None
        self.end = False
        self.currentState = INICIO
        self.previousState = None
        self.bebop = bebop
        self.client = None
        self.endMision = False
        self.messages = {i: [] for i in dir(enum) if not i.startswith('_')}
        self.assignedPOIs = {}
        self.messageMutex = Lock()
        self.idMessage = 1
        self.poisCritico = []
        self.poisVigilar = []
        self.isAlone = isAlone
        self.poiVigilarTimeoutDict = {}

    def execute(self):
        endExecutionTimer = Timer(TIMEOUT, self.isEndMision)
        endExecutionTimer.start()
        while not self.end:
            print("currentState: " + str(self.currentState))
            if self.currentState == INICIO:
                self.state = inicio.inicio(self.bebop, self.dataBuffer, self.previousState, self.poiVigilarTimeout, self.poiVigilarTimeoutDict, self.messages[self.currentState])
                # inicioState.execute(),
                # currentState = inicioState.getNextState()
            elif self.currentState == DESPEGAR:
                if self.previousState == INICIO:
                    self.client = self.dataBuffer
                    self.dataBuffer = self.initPoiPosition
                self.state = despegar.despegar(self.bebop, self.dataBuffer, self.previousState, self.poisCritico, self.messages[self.currentState])
                # currentState = despegarState.getNextState()
            elif self.currentState == EXPLORAR:
                self.state = explorar.explorar(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])
                # previousState = currentState;
                # currentState = explorarState.getNextState()
            elif self.currentState == ASIGNAR_POI:
                self.state = asignarPOI.asignarPOI(self.bebop, self.dataBuffer, self.previousState, self.client, self.idMessage, self.isAlone, self.assignedPOIs, self.checkMissionStatus, self.poisVigilar, self.messages[self.currentState])
                # currentState = asignarPOIState.getNextState()
            elif self.currentState == BATERIA_BAJA:
                self.state = bateriaBaja.bateriaBaja(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = bateriaBajaState.getNextState()
            elif self.currentState == BATERIA_CRITICA:
                self.state = bateriaCritica.bateriaCritica(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = bateriaCriticaState.getNextState()
            elif self.currentState == DESPLAZARSE:
                self.state = desplazarse.desplazarse(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])
                # desplazarseState.execute()
                # currentState = desplazarseState.getNextState()
            elif self.currentState == ACTUALIZAR_MAPA:
                self.state = actualizarMapa.actualizarMapa(self.bebop, self.dataBuffer, self.previousState, self.poisVigilar, self.poiVigilarTimeout, self.poiVigilarTimeoutDict, self.messages[self.currentState])

                # currentState = actualizarMapaState.getNextState()
            elif self.currentState == ENVIAR_MENSAJES:
                self.state = enviarMensajes.enviarMensajes(self.bebop, self.dataBuffer, self.client, self.assignedPOIs, self.endMision, self.isAlone, self.poisVigilar, self.poisCritico, self.messages[self.currentState])

                # currentState = enviarMensajesState.getNextState()
            elif self.currentState == POI_VIGILAR:
                self.state = POIVigilar.POIVigilar(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = POIVigilarState.getNextState()
            elif self.currentState == POI_CRITICO:
                self.state = POICritico.POICritico(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = POICriticoState.getNextState()
            elif self.currentState == CHEQUEAR_STATUS_MISION:
                self.state = chequearStatusMision.chequearStatusMision(self.bebop, self.dataBuffer, self.previousState, self.client, self.checkMissionStatus, self.poisVigilar, self.messages[self.currentState])
                # currentState = chequearStatusState.getNextState()
            elif self.currentState == ATERRIZAR:
                self.state = aterrizar.aterrizar(self.bebop, self.dataBuffer, self.previousState, self.endMision, self.messages[self.currentState])

            elif self.currentState == MISION_FINALIZADA:
                self.state = misionFinalizada.misionFinalizada(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

                # currentState = misionFinalizadaState.getNextState()
            elif self.currentState == CANCELAR_MISION:
                self.state = cancelarMision.cancelarMision(self.bebop, self.dataBuffer, self.previousState, self.idMessage, self.messages[self.currentState])

                # currentState = cancelarMisionState.getNextState()
            elif self.currentState == PING_SIN_CONEXION:
                self.state = pingSinConexion.pingSinConexion(self.bebop, self.dataBuffer, self.previousState, self.client, self.messages[self.currentState])

                # currentState = sinConexionState.getNextState()
            elif self.currentState == CARGAR:
                self.state = cargarBateria.cargarBateria(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

            elif self.currentState == ACTUALIZAR_MAPA_SIN_CONEXION:
                self.state = actualizarMapaSinConexion.actualizarMapaSinConexion(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

            elif self.currentState == DESPLAZARSE_SIN_CONEXION:
                self.state = desplazarseSinConexion.desplazarseSinConexion(self.bebop, self.dataBuffer, self.previousState, self.messages[self.currentState])

            elif self.currentState == FIN:
                self.state = fin.fin(self.bebop, self.dataBuffer, self.previousState, self.client, self.messages[self.currentState])
                self.end = True

            self.processState()

    def processState(self):
        self.dataBuffer = self.state.execute()
        self.messages[self.currentState] = []
        self.previousState = self.currentState
        self.currentState = self.state.getNextState()
        self.idMessage += 1

    def isEndMision(self):
        self.endMision = True

    # server related methods
    def handleMessage(self, message):
        self.messageMutex.acquire()
        print("handleMessage: ", message)
        if message["state"] == GENERAL:
            if message["message_type"] == UPDATE_MAP:
                self.bebop.updateSearchMap(message["content"])
            elif message["message_type"] == MISSION_ABORTED:
                self.checkPOIStatus(message["ip"], message["poi"])
        elif self.currentState == message["state"]:
            self.state.handleMessage(message)
        else:
            self.messages[message["state"]].append(message)
        self.messageMutex.release()

    def checkPOIStatus(self, ipDron, poi):
        if poi in self.assignedPOIs:
            if self.assignedPOIs[poi][0] == ipDron:
                self.POIsToAssign.append(poi)
            else:
                self.client.send_direct_message(createMessage(ASIGNAR_POI, POI_ALREADY_ASSIGNED, "go back to explore"), ipDron)

    def checkMissionStatus(self, poi):
        if (poi in self.assignedPOIs):
            self.poisToCcheck[poi] = self.assignedPOIs[poi]

    def poiVigilarTimeout(self, poi):
        print("poiVigilarTimeout: ", poi)
        self.poisVigilar.append(poi)
        poiCriticoTimer = Timer(TIMEOUT, self.poiCriticoTimeout, poi)
        poiCriticoTimer.start()

    def poiCriticoTimeout(self, poi):
        encontre = False
        for poiVigilar in self.poisVigilar:
            if poiVigilar == poi:
                encontre = True
                break
        if encontre:
            self.poisVigilar.remove(poi)
            self.poisCritico.append(poi)
