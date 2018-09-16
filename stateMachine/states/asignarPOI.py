from stateMachine.statesEnum import EXPLORAR, ASIGNAR_POI, CANCELAR_MISION
from utils import cartesianDistance, createMessage, convertTupleToString
from properties import DISTANCE_ENERGY_RATIO, LOW_BATTERY, WAIT_TIME, TIME_BETWEEN_POI_PING, SPHINX_SIMULATION
import threading
from connections.message_type import AVAILABLE, UNAVAILABLE, DISTANCE, RESULT, POI_ALREADY_ASSIGNED


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

            if available_battery - (distance / DISTANCE_ENERGY_RATIO) > LOW_BATTERY:
                message = createMessage(ASIGNAR_POI, AVAILABLE, self.bebop.ip)
                for ip in connected_drones:
                    self.client.send_message(message)
                self.availableDrones.append(self.bebop.ip)
            else:
                message = createMessage(ASIGNAR_POI, UNAVAILABLE, self.bebop.ip)
                for ip in connected_drones:
                    self.client.send_message(message)
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

            message2 = createMessage(ASIGNAR_POI, DISTANCE, dict({'ip': self.bebop.ip, 'distance': distance}))
            self.messageMutex.acquire()
            for ip in self.availableDrones:
                if ip != self.bebop.ip:
                    self.client.send_direct_message(message2, ip)
            self.messageMutex.release()
            timer2 = threading.Timer(WAIT_TIME, self.messageWaitTimeout)
            timer2.start()
            conditionMet = False
            self.availableDistances.append({"distance": distance, "ip": self.bebop.ip})
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

            self.messageMutex.acquire()
            print("self.availableDistances: ", self.availableDistances)
            for elem in self.availableDistances:
                if elem["distance"] < minDistance:
                    minDistance = elem["distance"]
                    minIp = elem["ip"]
                elif  elem["distance"] == minDistance:
                    if self.isLower(elem["ip"], minIp):
                        minDistance = elem["distance"]
                        minIp = elem["ip"]
            message3 = createMessage(ASIGNAR_POI, RESULT, minIp)
            for ip in self.availableDrones:
                self.client.send_direct_message(message3, ip)
            self.messageMutex.release()
            timer3 = threading.Timer(WAIT_TIME, self.messageWaitTimeout)
            timer3.start()
            conditionMet = False
            self.availableResults.append(minIp)
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
            print("self.availableResults: ",self.availableResults)
            for ip in self.availableDrones:
                count = 0
                for elem in self.availableResults:
                    if elem == ip:
                        count += 1
                if count > concensusValue:
                    concensusValue = count
                    concensus = ip
            self.messageMutex.release()
            if concensus == self.bebop.ip:
                self.result = self.poiType
                self.bebop.poi_position = self.poi
            self.assignedPOIs[convertTupleToString(self.poi)] = concensus
            timer2 = threading.Timer(TIME_BETWEEN_POI_PING, self.checkMissionStatus, (self.poi,))
            timer2.start()
            print("drone Asignado: ", concensus)
        print("POI ASignado: ", self.poi)
        return self.poi

    def messageWaitTimeout(self):
        self.timeout = True
        if self.messageWait.locked():
            self.messageWait.release()

    def isLower(self, ip1, ip2):
        if SPHINX_SIMULATION:
            print("isLower: ip1 ",ip1, " ip2 ", ip2)
            return int(ip1) < int(ip2)
        else:
            str1 = ip1.split(".")[3]
            str2 = ip2.split(".")[3]
            return int(str1) < int(str2)


    def handleMessage(self, message):
        print("handleMessage: ", message)
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
