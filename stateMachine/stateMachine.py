from stateMachine.statesEnum import INICIO, DESPEGAR, EXPLORAR, ASIGNAR_POI, BATERIA_BAJA, BATERIA_CRITICA, DESPLAZARSE,
ACTUALIZAR_MAPA, ENVIAR_MENSAJES, POI_VIGILAR, POI_CRITICO,
CHEQUEAR_STATUS_MISION, ATERRIZAR, MISION_FINALIZADA, SIN_CONEXION, CANCELAR_MISION, FIN
from stateMachine.states import actualizarMapa, asignarPOI, aterrizar, bateriaBaja, bateriaCritica,
cancelarMision, chequearStatus, despegar, desplazarse, enviarMensajes, explorar, fin, inicio,
misionFinalizada, POICritico, POIVigilar, sinConexion

end = False
currentState = INICIO
while !end:
    if currentState == INICIO:
        print("currentState: "+str(currentState))
        inicioState = inicio()

        currentState = inicioState.getNextState():
    elif currentState == DESPEGAR:
        print("currentState: "+str(currentState))
        despegarState = despegar()

        currentState = despegarState.getNextState()

    elif currentState == EXPLORAR:
        print("currentState: "+str(currentState))
        explorarState = explorar()
        currentState = explorarState.getNextState()
    elif currentState == ASIGNAR_POI:
        print("currentState: "+str(currentState))
        asignarPOIState = asignarPOI()

        currentState = asignarPOIState.getNextState()
    elif currentState == BATERIA_BAJA:
        print("currentState: "+str(currentState))
        bateriaBajaState = bateriaBaja()

        currentState = bateriaBajaState.getNextState()
    elif currentState == BATERIA_CRITICA:
        print("currentState: "+str(currentState))
        bateriaCriticaState = bateriaCritica()

        currentState = bateriaCriticaState.getNextState()
    elif currentState == DESPLAZARSE:
        print("currentState: "+str(currentState))
        desplazarseState = desplazarse()

        currentState = desplazarseState.getNextState()
    elif currentState == ACTUALIZAR_MAPA:
        print("currentState: "+str(currentState))
        actualizarMapaState = actualizarMapa()

        currentState = actualizarMapaState.getNextState()
    elif currentState == ENVIAR_MENSAJES:
        print("currentState: "+str(currentState))
        enviarMensajesState = enviarMensajes()

        currentState = enviarMensajesState.getNextState()
    elif currentState == POI_VIGILAR:
        print("currentState: "+str(currentState))
        POIVigilarState = POIVigilar()

        currentState = POIVigilarState.getNextState()
    elif currentState == POI_CRITICO:
        print("currentState: "+str(currentState))
        POICriticoState = POICritico()

        currentState = POICriticoState.getNextState()
    elif currentState == CHEQUEAR_STATUS_MISION:
        print("currentState: "+str(currentState))
        chequearStatusState = chequearStatus()

        currentState = chequearStatusState.getNextState()
    elif currentState == ATERRIZAR:
        print("currentState: "+str(currentState))
        aterrizarState = aterrizar()

        currentState = aterrizarState.getNextState()
    elif currentState == MISION_FINALIZADA:
        print("currentState: "+str(currentState))
        misionFinalizadaState = misionFinalizada()

        currentState = misionFinalizadaState.getNextState()
    elif currentState == CANCELAR_MISION:
        print("currentState: "+str(currentState))
        cancelarMisionState = cancelarMision()

        currentState = cancelarMisionState.getNextState()
    elif currentState == SIN_CONEXION:
        print("currentState: "+str(currentState))
        sinConexionState = sinConexion()

        currentState = sinConexionState.getNextState()
    elif currentState == FIN:
        print("currentState: "+str(currentState))
        finState = fin()
        end = True
