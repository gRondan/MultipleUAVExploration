from connections import connections
from flightplans import shittingHamster
import time

drone = shittingHamster.drone()
result = drone.explorar(0,0)
for i in range(1000):
    result = drone.explorar(result[0], result[1])
    #time.sleep(3)
