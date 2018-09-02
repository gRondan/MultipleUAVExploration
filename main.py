from flightplans import drone
import threading
from connections.server import server
from properties import HOME, INIT_POI_POSITION, POI_POSITIONS, FOREVER_ALONE, OBSTACLES
from stateMachine.stateMachine import stateMachine


def main(drone1):
    stateMachine1 = stateMachine(HOME, INIT_POI_POSITION, FOREVER_ALONE, drone1, OBSTACLES)
    stateMachine1.execute()
    server1 = server(drone1, stateMachine1)
    my_ip = server1.ip
    drone1.initialize(my_ip)
    client_handler = threading.Thread(
        target=server.run_server,
        args=(my_ip, drone1,)
    )
    client_handler.start()


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


drone1 = drone.drone(HOME)
drone1.bebop.connect(10)
connection = threading.Thread(
    target=main,
    args=(drone1,)
)
connection2 = threading.Thread(
    target=interface,
    args=(drone1,)
)
connection.start()
connection2.start()
