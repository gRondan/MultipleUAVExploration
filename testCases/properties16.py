from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp3s0"
RANGO_LARGO=1.81
RANGO_ANCHO=1.81
MAPA_LARGO=25.34
MAPA_ANCHO=28.96
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
POI_POSITIONS = [(5,11),(3,4),(11,0),(12,2),(0,9),(5,10),(1,8),(8,11)]
POI_TIMERS = [167,277,292,144,146,259,243,166]
POI_CRITICO_TIMERS = [89,64,111,96,80,62,68,107]
FOREVER_ALONE = None
OBSTACLES = [(6,7),(3,0),(2,8),(2,5),(9,14),(4,15),(9,10),(11,2),(10,6),(10,4),(9,5),(0,2),(12,7),(2,14),(4,9),(8,8),(10,12),(6,14),(10,15),(1,4),(1,9),(2,2),(5,13),(1,13),(10,5),(11,9),(1,5),(3,15),(12,6),(7,4),(10,14),(12,9),(1,6),(8,3),(9,9),(8,13),(9,3),(2,15),(7,7),(2,1),(1,3),(4,8),(2,4),(2,9),(10,3),(13,6),(13,12),(8,5),(5,15),(13,14),(8,7),(7,11),(11,7),(9,2),(12,13)]
SYNC_WAIT = 10
SPHINX_SIMULATION = False
ALGORITHM = SH_ORIGINAL
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = False
STREAMING_MODE_ON = True
ROTATE = False
