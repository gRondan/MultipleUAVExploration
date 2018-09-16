from flightplans import drone
import threading
from connections.server import server
from properties import HOME, INIT_POI_POSITION, FOREVER_ALONE, OBSTACLES, SPHINX_SIMULATION
from stateMachine.stateMachine import stateMachine

if SPHINX_SIMULATION:
    import matplotlib
    import matplotlib.pyplot as plt
    import time
    from matplotlib.colors import Normalize


def main(drone1):
    # stateMachine1 = stateMachine(HOME, INIT_POI_POSITION, FOREVER_ALONE, drone1, OBSTACLES)
    stateMachine1 = stateMachine(HOME, INIT_POI_POSITION, FOREVER_ALONE, drone1)
    server1 = server(drone1, stateMachine1)
    my_ip = server1.get_server_ip()
    drone1.initialize(my_ip)
    client_handler = threading.Thread(
        target=server1.run_server,
        args=()
    )
    client_handler.start()
    stateMachine1.execute()


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


def plotMatrix(drone1):
    matplotlib.use('TkAgg')
    plt.ion()
    plt.show()
    plt.suptitle("Cubrimiento del mapa para el dron " + str(drone1.ip))
    while True:
        plt.imshow(drone1.search_map, norm=Normalize(vmin=0, vmax=10, clip=True), cmap=plt.cm.RdYlGn)
        plt.draw()
        plt.pause(0.001)
        time.sleep(2)


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

if SPHINX_SIMULATION:
    connection3 = threading.Thread(
        target=plotMatrix,
        args=(drone1,)
    )
    connection3.start()
