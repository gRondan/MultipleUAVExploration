from pyparrot.Bebop import Bebop
import threading
import keyboard

drone1 = Bebop()
drone1.connect(10)


def interface(drone1):
    print('interface is ON')
    while not keyboard.is_pressed('esc') and not keyboard.is_pressed('esc'):
        if keyboard.is_pressed('l'):
            print('Landing')
            drone1.land()
        elif keyboard.is_pressed(' '):
            print('Taking off')
            drone1.safe_takeoff(10)
        elif keyboard.is_pressed('w'):
            print('Moving forward')
            drone1.fly_direct(roll=0, pitch=50, yaw=0, vertical_movement=0, duration=0.1)
        elif keyboard.is_pressed('s'):
            print('Moving backward')
            drone1.fly_direct(roll=0, pitch=-50, yaw=0, vertical_movement=0, duration=0.1)
        elif keyboard.is_pressed('a'):
            print('Moving left')
            drone1.fly_direct(roll=-50, pitch=0, yaw=0, vertical_movement=0, duration=0.1)
        elif keyboard.is_pressed('d'):
            print('Moving right')
            drone1.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=0.1)
        elif keyboard.is_pressed('left'):
            print('Turning left')
            drone1.fly_direct(roll=0, pitch=0, yaw=-50, vertical_movement=0, duration=0.1)
        elif keyboard.is_pressed('right'):
            print('Turning right')
            drone1.fly_direct(roll=0, pitch=0, yaw=50, vertical_movement=0, duration=0.1)
        elif keyboard.is_pressed('up'):
            print('Moving up')
            drone1.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=50, duration=0.1)
        elif keyboard.is_pressed('down'):
            print('Moving down')
            drone1.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-50, duration=0.1)

    drone1.land()
    drone1.disconnect()


connection = threading.Thread(
    target=interface,
    args=(drone1,)
)

connection.start()
