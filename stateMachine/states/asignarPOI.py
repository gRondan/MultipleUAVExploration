from stateMachine.statesEnum import EXPLORAR, ASIGNAR_POI, CANCELAR_MISION, GENERAL
from utils import cartesianDistance, createMessage, convertTupleToString, concatIpPort, parseIpPort
from properties import DISTANCE_ENERGY_RATIO, LOW_BATTERY, WAIT_TIME, TIME_BETWEEN_POI_PING, SPHINX_SIMULATION, SYNC_ASIGNARPOI_MSG
import threading
from connections.message_type import AVAILABLE, UNAVAILABLE, DISTANCE, RESULT, POI_ALREADY_ASSIGNED, POI_ASSIGNED


class asignarPOI():
    def __init__(self, bebop, dataBuffer, previousState, client, idMessage, isAlone, assignedPOIs, checkMissionStatus, messages):
        self.bebop = bebop
        self.previousState = previousState
        self.poi = dataBuffer["poi"]
        self.poiType = dataBuffer["type"]
        self.client = client
        self.isAlone = isAlone
        self.result = EXPLORAR
        self.messages = messages
        self.availableDrones = [elem['content'] for elem in messages if elem['message_type'] == AVAILABLE]
        self.unavailableDrones = [elem['content'] for elem in messages if elem['message_type'] == UNAVAILABLE]
        self.availableDistances = [elem['content'] for elem in messages if elem['message_type'] == DISTANCE]
        self.availableResults = [elem['content'] for elem in messages if elem['message_type'] == RESULT]
        self.poiAlreadyAssigned = [elem['content'] for elem in messages if elem['message_type'] == POI_ALREADY_ASSIGNED and elem['message_id'] == idMessage]
        self.timeout = False
        self.messageMutex = threading.Lock()
        self.messageWait = threading.Lock()
        self.blockHandleMessage = threading.Lock()
        self.idMessage = idMessage
        self.assignedPOIs = assignedPOIs
        self.checkMissionStatus = checkMissionStatus

    def getNextState(self):
        return self.result

    def execute(self):
        if self.isAlone:
            self.result = self.poiType
            self.bebop.poi_position = self.poi
            self.assignedPOIs[self.poi] = self.bebop.ip
        else:
            if len(self.poiAlreadyAssigned) > 0 and self.previousState == CANCELAR_MISION:
                return None

            if len(self.availableDistances) > 0 or len(self.availableResults) > 0:
                # im late to the party
                return None

            connected_drones = self.client.check_friends()
            distance = cartesianDistance(self.poi, self.bebop.current_position)
            available_battery = self.bebop.getBatteryPercentage()
            ipPort = dict({"ip": self.bebop.ip, "port": self.bebop.port})
            if available_battery - (distance / DISTANCE_ENERGY_RATIO) > LOW_BATTERY:
                message = createMessage(ASIGNAR_POI, AVAILABLE, ipPort)
                self.availableDrones.append(ipPort)
                for ipPort in connected_drones:
                    # antes estaba send_message
                    self.client.send_direct_message(message, ipPort["ip"], ipPort["port"])
            else:
                message = createMessage(ASIGNAR_POI, UNAVAILABLE, concatIpPort(self.bebop.ip, self.bebop.port))
                for ipPort in connected_drones:
                    # antes estaba send_message
                    self.client.send_direct_message(message, ipPort["ip"], ipPort["port"])
                return None

            timer1 = threading.Timer(WAIT_TIME, self.messageWaitTimeout)
            timer1.start()

            conditionMet = False
            while not conditionMet and not self.timeout:
                self.messageWait.acquire()
                if self.blockHandleMessage.locked():
                    self.blockHandleMessage.release()
                self.messageMutex.acquire()
                conditionMet = len(self.availableDrones) + len(self.unavailableDrones) - 1 >= len(connected_drones)
                self.messageMutex.release()

            self.timeout = False
            timer1.cancel()
            availableDronesNumber = len(self.availableDrones)
            distanceDict = dict({"distance": distance, "ip": self.bebop.ip, "port": self.bebop.port})
            message2 = createMessage(ASIGNAR_POI, DISTANCE, distanceDict)
            self.messageMutex.acquire()
            # for ip in self.availableDrones:
            #     if ip != self.bebop.ip:
            self.client.send_message(message2)
            self.messageMutex.release()
            timer2 = threading.Timer(SYNC_ASIGNARPOI_MSG, self.messageWaitTimeout)
            timer2.start()
            conditionMet = False
            self.availableDistances.append(distanceDict)
            while not conditionMet and not self.timeout:
                self.messageWait.acquire()
                if self.blockHandleMessage.locked():
                    self.blockHandleMessage.release()
                self.messageMutex.acquire()
                conditionMet = len(self.availableDistances) >= availableDronesNumber
                self.messageMutex.release()
            self.timeout = False
            timer2.cancel()
            minDistance = distance
            minIp = self.bebop.ip
            minPort = self.bebop.port

            self.messageMutex.acquire()
            minimoEncontrado = dict({"ip": minIp, "port": minPort})
            for elem in self.availableDistances:
                if elem["distance"] < minDistance:
                    minDistance = elem["distance"]
                    minIp = elem["ip"]
                    minPort = elem["port"]
                elif elem["distance"] == minDistance:
                    if self.isLower(elem, minimoEncontrado):
                        minDistance = elem["distance"]
                        minIp = elem["ip"]
                        minPort = elem["port"]
                        minimoEncontrado = dict({"ip": minIp, "port": minPort})
            # minimoEncontrado = dict({"ip": minIp, "port": minPort})
            message3 = createMessage(ASIGNAR_POI, RESULT, minimoEncontrado)
            for ipPort in self.availableDrones:
                if ipPort["ip"] != self.bebop.ip or ipPort["port"] != self.bebop.port:
                    self.client.send_direct_message(message3, ipPort["ip"], ipPort["port"])
            self.messageMutex.release()
            timer3 = threading.Timer(SYNC_ASIGNARPOI_MSG, self.messageWaitTimeout)
            timer3.start()
            conditionMet = False
            self.availableResults.append(minimoEncontrado)
            while not conditionMet and not self.timeout:
                self.messageWait.acquire()
                if self.blockHandleMessage.locked():
                    self.blockHandleMessage.release()
                self.messageMutex.acquire()
                conditionMet = len(self.availableResults) >= len(self.availableDrones)
                self.messageMutex.release()
            self.timeout = False
            timer3.cancel()

            concensus = ''
            concensusValue = 0
            self.messageMutex.acquire()
            for ipPort in self.availableDrones:
                count = 0
                for elem in self.availableResults:
                    if elem == ipPort["ip"]:
                        count += 1
                if count > concensusValue:
                    concensusValue = count
                    concensus = ipPort
                elif count == concensusValue:
                    if self.isLower(ipPort, concensus):
                        concensusValue = count
                        concensus = ipPort
            self.messageMutex.release()
            if concensus["ip"] == self.bebop.ip and concensus["port"] == self.bebop.port:
                self.result = self.poiType
                self.bebop.poi_position = self.poi
                message4 = createMessage(GENERAL, POI_ASSIGNED, convertTupleToString(self.poi))
                self.client.send_message(message4)
            timer2 = threading.Timer(TIME_BETWEEN_POI_PING, self.checkMissionStatus, (self.poi,))
            timer2.start()
            self.assignedPOIs[convertTupleToString(self.poi)] = concensus
            print("drone Asignado: ", concensus)
        print("POI ASignado: ", self.poi)
        return self.poi

    def messageWaitTimeout(self):
        self.timeout = True
        if self.messageWait.locked():
            self.messageWait.release()

    def isLower(self, ipPort1, ipPort2):
        if ipPort2 == "":
            return True
        # if SPHINX_SIMULATION:
        #     print("isLower: ip1 ",ip1, " ip2 ", ip2)
        #     return int(ip1) < int(ip2)
        # else:
        ip1 = ipPort1["ip"].split(".")[3]
        ip2 = ipPort2["ip"].split(".")[3]
        port1 = ipPort1["port"]
        port2 = ipPort2["port"]
        return (int(ip1) < int(ip2)) or (int(ip1) == int(ip2) and int(port1) < int(port2))


    def handleMessage(self, message):
        self.blockHandleMessage.acquire()
        self.messageMutex.acquire()
        if message["message_type"] == AVAILABLE:
            self.availableDrones.append(message["content"])
        elif message["message_type"] == UNAVAILABLE:
            self.unavailableDrones.append(message["content"])
        elif message["message_type"] == DISTANCE:
            self.availableDistances.append(message["content"])
        elif message["message_type"] == RESULT:
            self.availableResults.append(message["content"])
        elif message["message_type"] == POI_ALREADY_ASSIGNED and message['message_id'] == self.idMessage:
            self.poiAlreadyAssigned.append(message["content"])
        if self.messageWait.locked():
            self.messageWait.release()
        self.messageMutex.release()
