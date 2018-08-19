from connections import connections
from connections import client
from flightplans import drone, droneTest
from batteryEnum import LOW, CRITICAL, NORMAL
import time
import utils
import threading

#drone1 = drone.drone((0,0))
drone1 = droneTest.droneTest((23,31))

my_ip = connections.get_server_ip()
client_handler = threading.Thread(
    target=connections.run_server,
    args=(my_ip, drone1,)
)
client_handler.start()
client = client.client()
client.search_friends(my_ip)

drone1.take_off()

#result2= (23,31)
#drone2.updateSearchMap(result)
#drone1.updateSearchMap(result2)
for i in range(4000):
    new_position = drone1.explore()
    drone1.move(new_position)
    message = utils.convertTupleToString(drone1.current_position)
    client.send_message(message)

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
