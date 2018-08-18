from connections import connections
from flightplans import drone
from batteryEnum import LOW, CRITICAL, NORMAL
import time
import utils

drone1 = drone.drone((0,0))
drone2 = drone.drone((0,0))

my_ip = connections.get_server_ip()
connections.run_server(my_ip, drone2)
#result2= (23,31)
#drone2.updateSearchMap(result)
#drone1.updateSearchMap(result2)
for i in range(1000):
    drone1.explore()
    message = utils.convertTupleToString(drone1.current_position)
    connections.send_message(message)
    #drone2.updateSearchMap(result)
    #result2 = drone2.explorar(result2)
    #drone1.updateSearchMap(result2)
    if i == 200:
        drone1.battery_status = LOW
        print("es low")
    if i == 230:
        print("es critical")
        drone1.goHome()
    if drone1.current_position == drone1.home:
        drone1.battery_status = NORMAL
