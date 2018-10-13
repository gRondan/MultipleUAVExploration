import os
import enums
import time

algoritmos = [i for i in dir(enums) if not i.startswith('_')] # total: 3
ejecuciones = 10
instancias = 10

print("ALGORITMOS: ", algoritmos)

for algoritmo in algoritmos:
    cwd = os.path.join(os.getcwd(), "propertiesUpdater.py")
    cmd = cwd + ' ALGORITHM ' + algoritmo
    os.system('{} {}'.format('python', cmd))
    print('PROBANDO ALGORITMO: ', algoritmo)
    for instancia in range(instancias):
        for ejecucion in range(ejecuciones):
            cwd = os.path.join(os.getcwd(), "main.py")
            cmd = cwd + ' ' + str(instancia)
            print('ALGORITMO: {}, MAPA: {}, ITERACION: {}'.format(algoritmo, instancia, ejecucion))
            os.system('{} {}'.format('python', cmd))
