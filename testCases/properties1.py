from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp2s0"
RANGO_LARGO=1.81
RANGO_ANCHO=1.81
MAPA_LARGO=16.29
MAPA_ANCHO=45.25
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
POI_POSITIONS = [(0,2),(3,21),(6,23),(3,9),(6,14),(3,13),(8,5),(3,18),(0,12)]
POI_TIMERS = [217,125,267,278,266,274,178,269,136]
POI_CRITICO_TIMERS = [68,102,72,72,65,70,79,103,82]
FOREVER_ALONE = None
OBSTACLES = [(5,13),(2,15),(1,2),(5,4),(6,18),(7,20),(7,4),(3,24),(0,20),(8,19),(6,0),(5,5),(7,19),(5,7),(5,9),(0,7),(3,11),(8,22),(1,10),(3,12),(1,3),(1,11),(4,18),(0,4),(8,13),(4,14),(7,2),(3,8),(2,11),(1,9),(1,18),(6,19),(5,10),(1,0),(6,13),(7,15),(4,11),(1,1),(4,20)]
SYNC_WAIT = 10
SPHINX_SIMULATION = False
ALGORITHM = SH_ORIGINAL
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = False
STREAMING_MODE_ON = True
ROTATE = False
SUPER_MAIN = True
