from stateMachine.statesEnum import EXPLORAR, POI_VIGILAR, POI_CRITICO, ASIGNAR_POI, CANCELAR_MISION
from utils import cartesianDistance, createMessage
from properties import DISTANCE_ENERGY_RATIO, LOW_BATTERY, WAIT_TIME, POI_CRITICAL_EPSILON
import time
import threading
from connections.message_type import AVAILABLE, UNAVAILABLE, DISTANCE, RESULT, POI_ALREADY_ASSIGNED


class asignarPOI():
    def __init__(self, bebop, dataBuffer, previousState, client, idMessage, isAlone, messages):
        self.bebop = bebop
        self.previousState = previousState
        self.poi = dataBuffer
        self.client = client
        self.isAlone - isAlone
        self.result = 'unasign'
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

    def getNextState(self):
        if self.result == 'unasign':
            return EXPLORAR
        elif self.result == 'assign':
            return POI_VIGILAR
        elif self.result == 'critic_assign':
            return POI_CRITICO

    def execute(self):
        if self.isAlone:
            if time.time() - self.bebop.search_map[self.poi[0]][self.poi[1]] > POI_CRITICAL_EPSILON:
                self.result = 'assign'
            else:
                self.result = 'critic_assign'
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
                message = createMessage(ASIGNAR_POI, 'available', self.bebop.ip)
                for ip in connected_drones:
                    self.client.send_message(message)
            else:
                message = createMessage(ASIGNAR_POI, 'unavailable', self.bebop.ip)
                for ip in connected_drones:
                    self.client.send_message(message)
                return None

            timer1 = threading.Timer(WAIT_TIME, self.timeout)
            timer1.start()

            conditionMet = False
            while not conditionMet and not self.timeout:
                self.waitMessage.acquire()
                self.blockHandleMessage.release()
                self.messageMutex.acquire()
                conditionMet = len(self.availableDrones) + len(self.unavailableDrones) >= len(connected_drones)
                self.messageMutex.release()

            self.timeout = False
            timer1.cancel()
            availableDronesNumber = len(self.availableDrones)

            message2 = createMessage(ASIGNAR_POI, 'distance', {'ip': self.bebop.ip, 'distance': distance})
            self.messageMutex.acquire()
            for ip in self.availableDrones:
                self.client.send_direct_message(message2, ip)
            self.messageMutex.release()

            timer2 = threading.Timer(WAIT_TIME, self.timeout)
            timer2.start()
            conditionMet = False
            while not conditionMet and not self.timeout:
                self.waitMessage.acquire()
                self.blockHandleMessage.release()
                self.messageMutex.acquire()
                conditionMet = len(self.availableDistances) >= availableDronesNumber
                self.messageMutex.release()
            self.timeout = False
            timer2.cancel()

            minDistance = distance
            minIp = self.bebop.ip

            self.messageMutex.acquire()
            for elem in self.availableDistances:
                if elem["distance"] < minDistance:
                    minDistance = elem["distance"]
                    minIp = elem["ip"]

            message3 = createMessage(asignarPOI, 'result', minIp)
            for ip in self.availableDrones:
                self.client.send_direct_message(message3, ip)
            self.messageMutex.release()

            timer3 = threading.Timer(WAIT_TIME, self.timeout)
            timer3.start()
            conditionMet = False
            while not conditionMet and not self.timeout:
                self.waitMessage.acquire()
                self.blockHandleMessage.release()
                self.messageMutex.acquire()
                conditionMet = len(self.availableResults) >= len(self.availableDrones)
                self.messageMutex.release()

            self.timeout = False
            timer3.cancel()

            concensus = ''
            concensusValue = 0
            self.messageMutex.acquire()
            self.availableDrones.append(self.bebop.ip)
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
                if time.time() - self.bebop.search_map[self.poi[0]][self.poi[1]] > POI_CRITICAL_EPSILON:
                    self.result = 'critic_assign'
                else:
                    self.result = 'assign'
        return self.poi

    def timeout(self):
        self.timeout = True

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
        self.messageMutex.release()
        self.messageWait.release()
