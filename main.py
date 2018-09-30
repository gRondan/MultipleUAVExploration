from flightplans import drone
import threading
from connections.server import server
from properties import HOME, INIT_POI_POSITION, FOREVER_ALONE, OBSTACLES, SPHINX_SIMULATION, ALGORITHM, ACTIVATE_GRAPHIC_MAP
from stateMachine.stateMachine import stateMachine
from enums import RANDOM, SH_ORIGINAL, SH_TIMESTAMP
from executionStats import stats

if SPHINX_SIMULATION:
    import matplotlib
    import matplotlib.pyplot as plt
    import time
    from matplotlib.colors import Normalize


def main(drone1, logStats):
    # stateMachine1 = stateMachine(HOME, INIT_POI_POSITION, FOREVER_ALONE, drone1, OBSTACLES)
    stateMachine1 = stateMachine(HOME, INIT_POI_POSITION, FOREVER_ALONE, drone1, logStats)
    server1 = server(drone1, stateMachine1)
    my_ip = server1.get_server_ip()
    my_port = server1.get_server_port()
    drone1.initialize(my_ip, my_port)
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
    plt.ylim(0, int(drone1.mapa_ancho) - 1)
    plt.xlim(0, int(drone1.mapa_largo) - 1)
    while True:
        display_matrix = drone1.search_map
        vmin = 0
        vmax = 10
        if ALGORITHM == SH_TIMESTAMP:
            vmin = -256
            vmax = 0
            display_matrix = [[-(time.time() - drone1.search_map[i][j]) for j in range(int(drone1.mapa_largo))]for i in range(int(drone1.mapa_ancho))]
        plt.imshow(display_matrix, norm=Normalize(vmin=vmin, vmax=vmax, clip=True), cmap=plt.cm.RdYlGn)
        plt.draw()
        plt.pause(0.001)
        time.sleep(2)


drone1 = drone.drone(HOME)
drone1.bebop.connect(10)
logStats = stats.stats(drone1, 1)
connection = threading.Thread(
    target=main,
    args=(drone1, logStats)
)
connection2 = threading.Thread(
    target=interface,
    args=(drone1,)
)

connection.start()
connection2.start()

if SPHINX_SIMULATION and ACTIVATE_GRAPHIC_MAP:
    connection3 = threading.Thread(
        target=plotMatrix,
        args=(drone1,)
    )
    connection3.start()
