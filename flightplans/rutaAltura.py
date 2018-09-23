from threading import Thread
from flightplans import drone
import math

drone1 = drone.drone(HOME)

print("connecting")
success = drone1.bebop.connect(10)
print(success)

def measure(lat1, lon1, lat2, lon2):  # generally used geo measurement function
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000 # meters

def main(drone):
	print("RUTA 2 STARTING")
	drone.bebop.smart_sleep(1)

	drone.bebop.set_max_altitude(self.max_altitude)
	drone.bebop.ask_for_state_update()

	drone.bebop.safe_takeoff(10)

	drone.bebop.smart_sleep(1)
	verticalMove = drone.getDronVerticalAlignment()
	drone.bebop.move_relative(3, 0, verticalMove, 0)

	drone.bebop.smart_sleep(1)
	verticalMove = drone.getDronVerticalAlignment()
	drone.bebop.move_relative(0, -3, verticalMove, 0)

	drone.bebop.smart_sleep(1)
	verticalMove = drone.getDronVerticalAlignment()
	drone.bebop.move_relative(-3, 0, verticalMove, 0)

	drone.bebop.smart_sleep(1)
	verticalMove = drone.getDronVerticalAlignment()
	drone.bebop.move_relative(0, 3, verticalMove, 0)

	drone.bebop.smart_sleep(1)
	drone.bebop.safe_land(10)

	print("DONE - disconnecting")
	drone.disconnect()

def interface(drone1):
    command = input("prompt")
    print(command)
    while command != "q" or command == "Q":
        if command == "h" or command == "H":
            drone1.goHome()
        elif command == "l" or command == "L":
            drone1.land()
        command = input("prompt")
        print(command)
    drone1.land()
    drone1.disconnect()

connection = Thread(
    target=main,
    args=(drone1,)
)
connection2 = Thread(
    target=interface,
    args=(drone1,)
)

connection.start()
connection2.start()
