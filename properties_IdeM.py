from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="fd_veth1"
RANGO_LARGO=1.82
RANGO_ANCHO=1.82
MAPA_LARGO=18.2
MAPA_ANCHO=18.2
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
POI_POSITIONS = [(2,5), (7,7), (3,2)]
POI_TIMERS = [60, 120, 180]
POI_CRITICO_TIMERS = [20, 20, 20]
FOREVER_ALONE = None
OBSTACLES = [(1,4),(2,4),(3,4),(4,4), (6,6), (6,7), (6,8)]
SYNC_WAIT = 10
SPHINX_SIMULATION = True
ALGORITHM = SH_ORIGINAL
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = True