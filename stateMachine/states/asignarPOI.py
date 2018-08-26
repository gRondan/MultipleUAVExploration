from stateMachine.statesEnum import EXPLORAR, POI_VIGILAR, POI_CRITICO
from utils import cartesianDistance, createMessage
from properties import DISTANCE_ENERGY_RATIO, LOW_BATTERY
import time

class asignarPOI():
    def __init__(self, bebop, dataBuffer, previousState, messages, client):
        self.bebop = bebop
        self.previousState = previousState
        self.poi = dataBuffer
        self.client = client
        self.result = 'unasign'
        self.messages = messages
        self.availableDrones = [elem['content'] for elem in messages if elem['message_type'] == 'available']
        self.unavailableDrones = [elem['content'] for elem in messages if elem['message_type'] == 'unavailable']
        self.availableDistances = [elem['content'] for elem in messages if elem['message_type'] == 'distance']
        self.availableResults = [elem['content'] for elem in messages if elem['message_type'] == 'result']
        self.timeout = False

    def getNextState(self):
        if self.result == 'unasign':
            return EXPLORAR
        elif self.result == 'asign':
            return POI_VIGILAR
        elif self.result == 'critic_asign':
            return POI_CRITICO

    def execute(self):
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

        timer1 = Timer(properties.WAIT_TIME, self.timeout)
        timer1.start()
        while len(self.availableDrones) + len(self.unavailableDrones) < len(connected_drones) and not self.timeout:
            pass
        self.timeout = False
        timer1.cancel()
        availableDronesNumber = len(self.availableDrones)

        message2 = createMessage(ASIGNAR_POI, 'distance', {'ip': self.bebop.ip, 'distance': distance})
        for ip in self.availableDrones:
            self.client.send_direct_message(message2, ip)

        timer2 = Timer(properties.WAIT_TIME, self.timeout)
        timer2.start()
        while len(self.availableDistances) < availableDronesNumber and not self.timeout:
            pass
        self.timeout = False
        timer2.cancel()

        minDistance = distance
        minIp = self.bebop.ip
        for elem in self.availableDistances:
            if d["distance"] < minDistance:
                minDistance = d["distance"]
                minIp = d["ip"]

        message3 = createMessage(asignarPOI, 'result', minIp)
        for ip in self.availableDrones:
            self.client.send_direct_message(message3, ip)

        timer3 = Timer(properties.WAIT_TIME, self.timeout)
        timer3.start()
        while len(self.availableResults) < len(self.availableDrones) and not self.timeout:
            pass
        self.timeout = False
        timer3.cancel()

        concensus = ''
        concensusValue = 0
        for ip in self.availableDrones:
            count = 0
            for elem in self.availableResults:
                if elem == ip :
                    count += 1
            if count > concensusValue:
                concensusValue = count
                concensus = ip

        if concensus == self.bebop.ip:
            if time.time() - self.bebop.search_map[self.poi[0]][self.poi[1]] > properties.POI_CRITICAL_EPSILON:
                self.result = 'asign_critical'
            else:
                self.result = 'asign'

        return self.poi

    def timeout():
        self.timeout = True

    def handleMessage(self, message):
        if message["message_type"] == 'available':
            self.availableDrones.append(message["content"])
        if message["message_type"] == 'available':
            self.unavailableDrones.append(message["content"])
        if message["message_type"] == 'distance':
            self.availableDistances.append(message["content"])
        if message["message_type"] == 'result':
            self.availableResults.append(message["content"])
