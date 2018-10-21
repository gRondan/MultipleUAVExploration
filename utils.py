import math
import time
from properties import OBSTACLES, TIME_COVERAGE_REFRESH, ALGORITHM
from enums import SH_NO_GREEDY_TIMESTAMP, SH_TIMESTAMP, RANDOM
# CONSTANTS
ipPortSplitter = ":"


def printMatrix(matrix):
    a =1
    # print('****** PRINT MAPA ******')
    # print(getStringMatrix(matrix))
    # print('************************')


def getStringMatrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '-'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    return ('\n'.join(table))


def convertTupleToString(tupla):
    result = ""
    cnt = 0
    for i in tupla:
        result += str(i)
        if (cnt != len(tupla) - 1):
            result += ","
        cnt += 1
    return result


def convertTupleToStringParenthesis(tupla):
    result = "("
    cnt = 0
    for i in tupla:
        result += str(i)
        if (cnt != len(tupla) - 1):
            result += ","
        cnt += 1
    result += ")"
    return result


def convertStringToTuple(message):
    tupla = []
    for i in message.split(","):
        tupla.append(int(i))
    return tuple(tupla)


def convertTupleListToString(list1):
    strResult = '['
    for idx, tupla in enumerate(list1):
        strResult += convertTupleToStringParenthesis(tupla)
        if(idx != len(list1) - 1):
            strResult += ','
    strResult += ']'
    return strResult


def convertListToString(list1):
    strResult = '['
    for idx, elem in enumerate(list1):
        strResult += str(elem)
        if(idx != len(list1) - 1):
            strResult += ','
    strResult += ']'
    return strResult


def cartesianDistance(tuple1, tuple2):
    return math.sqrt((tuple2[1] - tuple1[1])**2 + (tuple2[0] - tuple1[0])**2)


def angleDifference(tuple1, tuple2, current_rotation):
    # tuple3 = (tuple1[0] + math.cos(current_rotation), tuple1[1] + math.sin(current_rotation))
    # d12, d13, d23 = cartesianDistance(tuple1, tuple2), cartesianDistance(tuple1, tuple3), cartesianDistance(tuple2, tuple3)
    # return math.acos((d12**2 + d13**2 - d23**2) / (2 * d12 * d13))
    angle = 0
    dx, dy = tuple2[0] - tuple1[0], tuple2[1] - tuple1[1]
    if dx > 0:
        if dy > 0:
            angle = math.pi / 4
        elif dy == 0:
            angle = math.pi / 2
        elif dy < 0:
            angle = math.pi * 3 / 4
    elif dx == 0:
        if dy > 0:
            angle = 0
        elif dy < 0:
            angle = math.pi
    elif dx < 0:
        if dy > 0:
            angle = - math.pi / 4
        elif dy == 0:
            angle = - math.pi / 2
        elif dy < 0:
            angle = math.pi * 3 / 4
    return current_rotation - angle


def getClosestPOI(current_position, pois):
    if len(pois) == 0:
        return None
    minPOI = pois[0]
    minDistance = cartesianDistance(pois[0], current_position)
    for poi in pois:
        distance = cartesianDistance(poi, current_position)
        if distance < minDistance:
            minPOI = poi
            minDistance = distance
    return minPOI


def createMessage(state, message_type, message_content, idMessage=0):
    return dict({"state": state, "message_type": message_type, "content": message_content, "message_id": idMessage})


def concatIpPort(ip, port):
    return ip + ipPortSplitter + port


def parseIpPort(ipPort):
    return dict({"ip": ipPort.split(ipPortSplitter)[0], "port": ipPort.split(ipPortSplitter)[1]})


def getMapCoverage(drone, init_largo, end_largo, init_ancho, end_ancho):
    totalMap = (end_largo - init_largo) * (end_ancho - init_ancho)
    isTimer = ALGORITHM == SH_TIMESTAMP or ALGORITHM == SH_NO_GREEDY_TIMESTAMP or ALGORITHM == RANDOM
    totalMap -= len(OBSTACLES)
    contSinExplorar = 0
    currentTime = time.time()
    for i in range(int(init_ancho), int(end_ancho)):
        for j in range(int(init_largo), int(end_largo)):
            if isTimer:
                timeBetweenLastVisit = currentTime - drone.search_map[i][j]
                firstTime = drone.search_map[i][j] == drone.init_time
                # print("timeBetweenLastVisit: ", timeBetweenLastVisit)
                if timeBetweenLastVisit < TIME_COVERAGE_REFRESH and not firstTime:
                    contSinExplorar += 1
            elif drone.search_map[i][j] > drone.countIter:
                contSinExplorar += 1
    return (contSinExplorar * 100) // totalMap
