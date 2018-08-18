

from pyparrot.Bebop import Bebop

bebop = Bebop()

print("connecting")
success = bebop.connect(10)
print(success)

print("sleeping")
bebop.smart_sleep(5)

bebop.ask_for_state_update()

bebop.safe_takeoff(10)

bebop.smart_sleep(5)
bebop.safe_land(10)

print("DONE - disconnecting")
bebop.disconnect()
