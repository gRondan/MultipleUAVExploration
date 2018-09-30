import os
import enums
import time

algoritmos = [getattr(enums, i) for i in dir(enums)] # total: 3
ejecuciones = 10
instancias = 10

for algoritmo in algoritmos:
    for instancia in range(instancias):
        for ejecucion in range(ejecuciones):
            cwd = os.path.join(os.getcwd(), "main.py")
            cmd = cwd + ' ' + str(instancia)
            print("COMMAND: ", cmd)
            os.system('{} {}'.format('python', cmd))
            print('TERMINEEEEEEEEEE')
