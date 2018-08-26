from flightplans import drone, droneTest
import threading
from properties import HOME, INIT_POI_POSITION, POI_POSITIONS
from stateMachine import stateMachine


def main(self):
    stateMachine1 = stateMachine(HOME, INIT_POI_POSITION, POI_POSITIONS)
    stateMachine1.execute()


drone1 = drone.drone(HOME)
drone1.connect()
connection = threading.Thread(
    target=main,
    args=(drone1,)
)
connection.start()
