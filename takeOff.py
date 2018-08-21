from pyparrot.Bebop import Bebop
import time


bebop = Bebop()
bebop.connect(10)
bebop.ask_for_state_update()
time.sleep(2)
bebop.safe_takeoff(10)
