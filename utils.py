import math


def printMatrix(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '-'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


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
