import re
import sys
from random import randint, sample, choice
from utils import convertTupleListToString, convertListToString
from itertools import product

INSTANCE_NUMBER = 30
SQUARE_SIZE = 1.81
if(len(sys.argv) > 1):
    INSTANCE_NUMBER = sys.argv[1]
if(len(sys.argv) > 2):
    SQUARE_SIZE = sys.argv[2]

content = ''
with open('baseProperties.py', 'r') as properties:
    content = properties.read()

for it in range(INSTANCE_NUMBER):
    # generar tamaño mapa
    cantLargo = randint(5, 30)
    cantAncho = randint(5, 30)
    largo = cantLargo * SQUARE_SIZE
    ancho = cantAncho * SQUARE_SIZE
    new_content = re.sub(r'MAPA_LARGO.*', 'MAPA_LARGO=' + str(largo), content)
    new_content = re.sub(r'MAPA_ANCHO.*', 'MAPA_ANCHO=' + str(ancho), new_content)
    new_content = re.sub(r'RANGO_LARGO.*', 'RANGO_LARGO=' + str(SQUARE_SIZE), new_content)
    new_content = re.sub(r'RANGO_ANCHO.*', 'RANGO_ANCHO=' + str(SQUARE_SIZE), new_content)

    # generar obstaculos
    result = []
    # sin obstaculos
    if(it % 3 == 0):
        strResult = convertTupleListToString(result)
    # con obstaculos aleatorios
    elif(it % 3 == 1):
        cantObstaculos = randint(int(cantLargo*cantAncho*0.1), int(cantLargo*cantAncho*0.3))
        positions = [(i,j) for i, j in product(range(cantLargo), range(cantAncho))]
        result = sample(positions, cantObstaculos)
    # con obstaculos en forma de pared
    elif(it % 3 == 2):
        cantObstaculos = randint(int(cantLargo*cantAncho*0.1), int(cantLargo*cantAncho*0.3))
        while(len(result) < cantObstaculos):
            direccionPared = choice(['horizontal', 'vertical'])
            largoPared = 0
            positions = []
            if (direccionPared == 'horizontal'):
                largoPared = randint(int(cantLargo*0.3), int(cantLargo*0.6))
                posicionInicio = randint(0, cantLargo - 1 - largoPared)
                columna = randint(0, cantAncho - 1)
                positions = [(i, columna) for i in range(posicionInicio, posicionInicio + largoPared - 1)]
            else:
                largoPared = randint(int(cantAncho*0.3), int(cantAncho*0.6))
                posicionInicio = randint(0, cantAncho - 1 - largoPared)
                fila = randint(0, cantLargo - 1)
                positions = [(fila, i) for i in range(posicionInicio, posicionInicio + largoPared - 1)]
            for tupla in positions:
                if(not tupla in result):
                    result.append(tupla)

    strResult = convertTupleListToString(result)
    new_content = re.sub(r'OBSTACLES.*', 'OBSTACLES = ' + strResult, new_content)

    # pois
    cantPois = randint(0, int(cantLargo*cantAncho*0.05))
    positions = [(i,j) for i, j in product(range(cantLargo), range(cantAncho)) if (i,j) not in result]
    poiResult = sample(positions, cantPois)
    poiTimers = []
    poiCriticalTimers = []
    for i in range(cantPois):
        poiTimers.append(randint(120, 300))
        poiCriticalTimers.append(randint(60, 120))

    strResultPois = convertTupleListToString(poiResult)
    new_content = re.sub(r'POI_POSITIONS.*', 'POI_POSITIONS = ' + strResultPois, new_content)
    strResultPoisTimers = convertListToString(poiTimers)
    new_content = re.sub(r'POI_TIMERS.*', 'POI_TIMERS = ' + strResultPoisTimers, new_content)
    strResultPoisCriticalTimers = convertListToString(poiCriticalTimers)
    new_content = re.sub(r'POI_CRITICO_TIMERS.*', 'POI_CRITICO_TIMERS = ' + strResultPoisCriticalTimers, new_content)

    with open('testCases/properties' + str(it) + '.py', 'w') as new_properties:
        new_properties.write(new_content)
