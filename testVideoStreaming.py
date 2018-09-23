from threading import Thread
from flightplans import drone
from properties import HOME
import math

drone1 = drone.drone(HOME)

print("connecting")
success = drone1.bebop.connect(10)
print(success)
drone1.initialize("192.168.42.1", "4444")

# def main(drone):
#     drone.bebop.smart_sleep(1)
#     drone.bebop.ask_for_state_update()
#     print("STARTING STREAMING...")
#     drone.bebop.set_picture_format('jpeg')
#     drone.bebop.set_video_resolutions('rec720_stream720')
#     drone.bebop.start_video_stream()
#     print("STREAMING STARTED: 2 minutos")
#     drone.bebop.smart_sleep(120)
#     print("STOPPING STREAMING...")
#     drone.bebop.stop_video_stream()
#     print("STREAMING STOPPED")
#     drone.disconnect()

# def interface(drone1):
#     command = input("prompt")
#     print(command)
#     while command != "q" or command == "Q":
#         if command == "h" or command == "H":
#             drone1.goHome()
#         elif command == "l" or command == "L":
#             drone1.land()
#         command = input("prompt")
#         print(command)
#     drone1.disconnect()

# connection = Thread(
#     target=main,
#     args=(drone1,)
# )
# connection2 = Thread(
#     target=interface,
#     args=(drone1,)
# )

# connection.start()
# connection2.start()
