from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM, SH_NO_GREEDY

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp3s0"
RANGO_LARGO=10
RANGO_ANCHO=18
MAPA_LARGO=50
MAPA_ANCHO=90
LOW_BATTERY=10
CRITICAL_BATTERY=5
TIME_BETWEEN_POI_PING=20
TIMEOUT=1200
DISTANCE_ENERGY_RATIO=10
WAIT_TIME = 10
SYNC_ASIGNARPOI_MSG = 2
HOME = (0,0)
INIT_POI_POSITION = None
INIT_POI_POSITION_CRITICO = None
POI_POSITIONS = [(5,1),(5,2),(1,3)]
POI_TIMERS = [360,300,360]
POI_CRITICO_TIMERS = [60,60,60]
FOREVER_ALONE = None
OBSTACLES = [(2,0), (0,2), (2, 4), (3, 2), (4, 2)]
SYNC_WAIT = 10
SPHINX_SIMULATION = True
ALGORITHM = SH_NO_GREEDY
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = False
STREAMING_MODE_ON = False
ROTATE = False