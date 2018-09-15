from threading import Thread
from pyparrot.Bebop import Bebop
import math

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

def measure(lat1, lon1, lat2, lon2):  # generally used geo measurement function
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * math.pi / 180 - lat1 * math.pi / 180
    dLon = lon2 * math.pi / 180 - lon1 * math.pi / 180
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d * 1000 # meters

def main(bebop):
	print("RUTA 1 STARTING")
	bebop.smart_sleep(1)

	bebop.ask_for_state_update()

	bebop.safe_takeoff(10)

	bebop.smart_sleep(1)
	bebop.move_relative(5, 0, 0, 0)

	bebop.smart_sleep(1)
	bebop.move_relative(0, 5, 0, 0)

	bebop.smart_sleep(1)
	bebop.move_relative(2, 0, 0, 0)

	bebop.smart_sleep(1)
	bebop.move_relative(0, 0, 0, math.pi / 2)

	bebop.smart_sleep(1)
	bebop.move_relative(2, 0, 0, 0)

	bebop.smart_sleep(1)
	bebop.move_relative(0, 0, 0, math.pi / 2)

	bebop.smart_sleep(1)
	bebop.move_relative(2, 0, 0, 0)

	bebop.smart_sleep(1)
	bebop.move_relative(0, 0, 0, math.pi / 2)

	bebop.smart_sleep(1)
	bebop.move_relative(2, 0, 0, 0)

	bebop.smart_sleep(1)
	bebop.move_relative(0, 0, 0, -math.pi / 2)

	bebop.smart_sleep(1)
	bebop.move_relative(5, 0, 0, 0)

	bebop.smart_sleep(1)
	bebop.safe_land(10)

	print("DONE - disconnecting")
	bebop.disconnect()

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
    drone1.bebop.disconnect()

connection = Thread(
    target=main,
    args=(bebop,)
)
connection2 = Thread(
    target=interface,
    args=(bebop,)
)

connection.start()
connection2.start()
