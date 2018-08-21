from stateMachine.states import INICIO, DESPEGAR, EXPLORAR, ASIGNAR_POI, BATERIA_BAJA, BATERIA_CRITICA, DESPLAZARSE,
ACTUALIZAR_MAPA, ENVIAR_MENSAJES, POI_VIGILAR, POI_CRITICO,
CHEQUEAR_STATUS_MISION, ATERRIZAR, MISION_FINALIZADA, SIN_CONEXION, CANCELAR_MISION, FIN
from stateMachine.states import actualizarMapa, asignarPOI, aterrizar, bateriaBaja, bateriaCritica,
cancelarMision, chequearStatus, despegar, desplazarse, enviarMensajes, explorar, fin, inicio,
misionFinalizada, POICritico, POIVigilar, sinConexion

end = False
actualState = INICIO
while !end:
    if actualState == INICIO:
        print("actualState: "+str(actualState))
        inicioState = inicio()

        actualState = inicioState.getNextState():
    elif actualState == DESPEGAR:
        print("actualState: "+str(actualState))
        despegarState = despegar()

        actualState = despegarState.getNextState()

    elif actualState == EXPLORAR:
        print("actualState: "+str(actualState))
        explorarState = explorar()
        actualState = explorarState.getNextState()
    elif actualState == ASIGNAR_POI:
        print("actualState: "+str(actualState))
        asignarPOIState = asignarPOI()

        actualState = asignarPOIState.getNextState()
    elif actualState == BATERIA_BAJA:
        print("actualState: "+str(actualState))
        bateriaBajaState = bateriaBaja()

        actualState = bateriaBajaState.getNextState()
    elif actualState == BATERIA_CRITICA:
        print("actualState: "+str(actualState))
        bateriaCriticaState = bateriaCritica()

        actualState = bateriaCriticaState.getNextState()
    elif actualState == DESPLAZARSE:
        print("actualState: "+str(actualState))
        desplazarseState = desplazarse()

        actualState = desplazarseState.getNextState()
    elif actualState == ACTUALIZAR_MAPA:
        print("actualState: "+str(actualState))
        actualizarMapaState = actualizarMapa()

        actualState = actualizarMapaState.getNextState()
    elif actualState == ENVIAR_MENSAJES:
        print("actualState: "+str(actualState))
        enviarMensajesState = enviarMensajes()

        actualState = enviarMensajesState.getNextState()
    elif actualState == POI_VIGILAR:
        print("actualState: "+str(actualState))
        POIVigilarState = POIVigilar()

        actualState = POIVigilarState.getNextState()
    elif actualState == POI_CRITICO:
        print("actualState: "+str(actualState))
        POICriticoState = POICritico()

        actualState = POICriticoState.getNextState()
    elif actualState == CHEQUEAR_STATUS_MISION:
        print("actualState: "+str(actualState))
        chequearStatusState = chequearStatus()

        actualState = chequearStatusState.getNextState()
    elif actualState == ATERRIZAR:
        print("actualState: "+str(actualState))
        aterrizarState = aterrizar()

        actualState = aterrizarState.getNextState()
    elif actualState == MISION_FINALIZADA:
        print("actualState: "+str(actualState))
        misionFinalizadaState = misionFinalizada()

        actualState = misionFinalizadaState.getNextState()
    elif actualState == CANCELAR_MISION:
        print("actualState: "+str(actualState))
        cancelarMisionState = cancelarMision()

        actualState = cancelarMisionState.getNextState()
    elif actualState == SIN_CONEXION:
        print("actualState: "+str(actualState))
        sinConexionState = sinConexion()

        actualState = sinConexionState.getNextState()
    elif actualState == FIN:
        print("actualState: "+str(actualState))
        finState = fin()
        end = True
