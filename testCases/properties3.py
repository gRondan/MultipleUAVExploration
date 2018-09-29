from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp3s0"
RANGO_LARGO=1.81
RANGO_ANCHO=1.81
MAPA_LARGO=52.49
MAPA_ANCHO=39.82
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
POI_POSITIONS = [(26,10),(24,13),(2,4),(0,16),(8,14),(4,16)]
POI_TIMERS = [174,250,291,237,206,235]
POI_CRITICO_TIMERS = [88,114,116,92,74,109]
FOREVER_ALONE = None
OBSTACLES = []
SYNC_WAIT = 10
SPHINX_SIMULATION = False
ALGORITHM = SH_ORIGINAL
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = False
STREAMING_MODE_ON = True
ROTATE = False
