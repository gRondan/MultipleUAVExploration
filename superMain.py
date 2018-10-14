import os
import enums
import time

algoritmos = [i for i in dir(enums) if not i.startswith('_')] # total: 3
ejecuciones = 4
# las instancias y los algoritmos arrancan en el 0 y van agarran el intervalo [min, max)
instancia_min = 3
instancia_max = 4
algoritmo_min = 1
algoritmo_max = 2
ejecucion_inicial = 2

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
                cwd = os.path.join(os.getcwd(), "main.py")
                cmd = cwd + ' ' + str(instancia)
                print('ALGORITMO: {}, MAPA: {}, ITERACION: {}'.format(algoritmo, instancia, ejecucion))
                os.system('{} {}'.format('python', cmd))
            ejecucion_inicial = 0
