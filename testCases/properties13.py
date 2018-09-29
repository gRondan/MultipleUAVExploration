from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp3s0"
RANGO_LARGO=1.81
RANGO_ANCHO=1.81
MAPA_LARGO=14.48
MAPA_ANCHO=21.72
LOW_BATTERY=10
CRITICAL_BATTERY=5
TIME_BETWEEN_POI_PING=20
TIMEOUT=60000
DISTANCE_ENERGY_RATIO=10
WAIT_TIME = 10
SYNC_ASIGNARPOI_MSG = 2
HOME = (5,5)
INIT_POI_POSITION = None
INIT_POI_POSITION_CRITICO = None
POI_POSITIONS = [(1,7),(0,11),(3,1),(1,9)]
POI_TIMERS = [143,143,283,223]
POI_CRITICO_TIMERS = [75,70,115,83]
FOREVER_ALONE = None
OBSTACLES = [(3,9),(2,1),(1,11),(0,6),(6,7),(5,9),(0,4),(4,4),(6,1),(6,4),(4,0),(6,11),(3,4),(7,4),(5,2),(3,11),(5,10)]
SYNC_WAIT = 10
SPHINX_SIMULATION = False
ALGORITHM = SH_ORIGINAL
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = False
STREAMING_MODE_ON = True
ROTATE = False
