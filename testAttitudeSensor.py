from flightplans import drone
from properties import HOME
import time

def main():
    drone1 = drone.drone(HOME)
    drone1.bebop.connect(10)
    drone1.bebop.ask_for_state_update()

    def sensorCallback(drone):
        print("bebop.sensors.attitude: " + str(drone.bebop.sensors.sensors_dict["AltitudeChanged_altitude"]))

    drone1.bebop.set_user_sensor_callback(sensorCallback, drone1)
    drone1.bebop.safe_takeoff(10)
    time.sleep(10)
    drone1.bebop.safe_land(10)

main()