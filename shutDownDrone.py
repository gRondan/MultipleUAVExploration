from pyparrot.Bebop import Bebop
import time

exit = False
while not exit:
    try:
        bebop = Bebop()
        bebop.connect(10)
        bebop.ask_for_state_update()
        time.sleep(2)
        bebop.safe_land(10)
        exit = True
    except:
        pass
