import math

# CONSTANTS
ipPortSplitter = ":"


def printMatrix(matrix):
    print('****** PRINT MAPA ******')
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '-'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
    print('************************')


def convertTupleToString(tupla):
    result = ""
    cnt = 0
    for i in tupla:
        result += str(i)
        if (cnt != len(tupla) - 1):
            result += ","
        cnt += 1
    return result


def convertStringToTuple(message):
    tupla = []
    for i in message.split(","):
        tupla.append(int(i))
    return tuple(tupla)


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
