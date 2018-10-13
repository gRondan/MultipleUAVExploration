from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp2s0"
RANGO_LARGO=1.81
RANGO_ANCHO=1.81
MAPA_LARGO=18.1
MAPA_ANCHO=18.1
LOW_BATTERY=10
CRITICAL_BATTERY=5
TIME_BETWEEN_POI_PING=20
TIMEOUT=60
DISTANCE_ENERGY_RATIO=10
WAIT_TIME = 10
SYNC_ASIGNARPOI_MSG = 2
HOME = (5,5)
INIT_POI_POSITION = None
INIT_POI_POSITION_CRITICO = None
POI_POSITIONS = [(9,8),(2,4),(3,1)]
POI_TIMERS = [290,225,278]
POI_CRITICO_TIMERS = [95,91,68]
FOREVER_ALONE = True
OBSTACLES = []
SYNC_WAIT = 10
SPHINX_SIMULATION = True
ALGORITHM = SH_ORIGINAL
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = True
STREAMING_MODE_ON = False
ROTATE = False
SUPER_MAIN = True
