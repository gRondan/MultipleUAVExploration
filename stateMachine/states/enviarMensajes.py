class enviarMensajes():
    def __init__(self):

    def getNextState():

        if enviarMensajesTransitions.isAsignarPOI():
            actualState = ASIGNAR_POI
        elif enviarMensajesTransitions.isPOIVigilar():
            actualState = POI_VIGILAR
        elif enviarMensajesTransitions.isChequearStatusMision():
            actualState = CHEQUEAR_STATUS_MISION
        elif enviarMensajesTransitions.isExplorar():
            actualState = EXPLORAR
        elif enviarMensajesTransitions.isBateriaBaja():
            actualState = BATERIA_BAJA
        elif enviarMensajesTransitions.isBateriaCritica():
