from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM, SH_NO_GREEDY

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp3s0"
RANGO_LARGO=10
RANGO_ANCHO=18
MAPA_LARGO=80
MAPA_ANCHO=144
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
POI_POSITIONS = [(5,5), (4,6), (7,7)]
POI_TIMERS = [420, 300, 600]
POI_CRITICO_TIMERS = [60, 60, 60]
FOREVER_ALONE = None
OBSTACLES = [(3,1), (4,1), (6,2), (7, 2), (6, 3), (7,3), (2,5), (3,5), (2,6), (3,6), (2,7), (3,7)]
SYNC_WAIT = 10
SPHINX_SIMULATION = True
ALGORITHM=RANDOM
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = False
STREAMING_MODE_ON = False
ROTATE = False
TIME_COVERAGE_REFRESH = 600
SUPER_MAIN=True
COVERAGE_THRESHOLD = 20
MIN_ACCEPTABLE_COVERAGE = 90
