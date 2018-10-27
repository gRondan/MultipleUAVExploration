import os
import enums
import time
from enums import SH_TIMESTAMP, RANDOM, SH_NO_GREEDY_TIMESTAMP

algoritmos = [SH_TIMESTAMP, RANDOM, SH_NO_GREEDY_TIMESTAMP]
ejecuciones = 1
# las instancias y los algoritmos arrancan en el 0 y van agarran el intervalo [min, max)
instancia_min = 11
instancia_max = 21
algoritmo_min = 0
algoritmo_max = 3
ejecucion_inicial = 0

print("ALGORITMOS: ", algoritmos)

for index, algoritmo in enumerate(algoritmos):
    if index in range(algoritmo_min, algoritmo_max):
        cwd2 = os.path.join(os.getcwd(), "propertiesUpdater.py")
        cmd2 = cwd2 + ' ALGORITHM ' + algoritmo
        os.system('{} {}'.format('python', cmd2))
        print(cmd2)
        print('PROBANDO ALGORITMO: ', algoritmo)
        for instancia in range(instancia_min, instancia_max):
            for ejecucion in range(ejecucion_inicial, ejecuciones):
                with open('superMainLock.txt', 'a') as f:
                    f.write('LOCK')
                cwd = os.path.join(os.getcwd(), "main.py")
                cmd = cwd + ' ' + str(instancia) + " " + str(ejecucion)
                print('ALGORITMO: {}, MAPA: {}, ITERACION: {}'.format(algoritmo, instancia, ejecucion))
                os.system('{} {}'.format('python', cmd))
                content = ''
                with open('superMainLock.txt', 'r') as f:
                    content = f.read()
                content = content.replace('LOCK', '', 1)
                with open('superMainLock', 'w') as f:
                    f.write(content)
                while content != '':
                    with open('superMainLock.txt', 'r') as f:
                        content = f.read()
            ejecucion_inicial = 0
