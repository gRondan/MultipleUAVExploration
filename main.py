from flightplans import drone
import threading
from connections.server import server
from properties import HOME, INIT_POI_POSITION, FOREVER_ALONE
from stateMachine.stateMachine import stateMachine


def main(drone1):
    stateMachine1 = stateMachine(HOME, INIT_POI_POSITION, FOREVER_ALONE, drone1)
    stateMachine1.execute()
    server1 = server(drone1, stateMachine1)
    my_ip = server1.ip
    drone1.initialize(my_ip)
    client_handler = threading.Thread(
        target=server.run_server,
        args=(my_ip, drone1,)
    )
    client_handler.start()


drone1 = drone.drone(HOME)
drone1.bebop.connect(10)
connection = threading.Thread(
    target=main,
    args=(drone1,)
)
connection.start()
