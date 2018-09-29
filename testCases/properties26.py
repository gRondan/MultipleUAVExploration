from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp3s0"
RANGO_LARGO=1.81
RANGO_ANCHO=1.81
MAPA_LARGO=48.870000000000005
MAPA_ANCHO=50.68
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
POI_POSITIONS = [(11,11),(11,8),(10,1),(21,21),(2,12),(23,9),(23,4)]
POI_TIMERS = [202,224,286,168,166,267,274]
POI_CRITICO_TIMERS = [85,66,77,103,76,104,69]
FOREVER_ALONE = None
OBSTACLES = [(0,9),(1,9),(2,9),(3,9),(4,9),(5,9),(6,9),(7,9),(8,9),(9,9),(10,9),(11,9),(10,23),(11,23),(12,23),(13,23),(14,23),(15,23),(16,23),(17,23),(18,23),(19,23),(6,3),(7,3),(8,3),(9,3),(10,3),(11,3),(12,3),(13,3),(14,3),(15,3),(16,3),(17,3),(18,3),(19,3),(20,3),(17,2),(17,4),(17,5),(17,6),(17,7),(17,8),(17,9),(17,10),(17,11),(17,12),(17,13),(12,6),(13,6),(14,6),(15,6),(16,6),(18,6),(19,6),(7,23),(8,23),(9,23),(8,13),(9,13),(10,13),(11,13),(12,13),(13,13),(14,13),(15,13),(16,13),(5,5),(5,6),(5,7),(5,8),(5,10),(5,11),(5,12),(5,13),(5,14),(5,15),(5,16),(17,1),(17,14),(3,10),(4,10),(6,10),(7,10),(8,10),(9,10),(10,10),(11,10),(12,10),(13,10),(14,10),(15,10),(7,7),(7,8),(7,11),(7,12),(7,13),(7,14),(8,2),(8,4),(8,5),(8,6),(8,7),(8,8),(18,11),(18,12),(18,13),(18,14),(18,15),(18,16),(18,17),(18,18),(7,15),(11,5),(12,5),(13,5),(14,5),(15,5),(16,5),(18,5),(19,5),(20,5),(21,5),(22,5),(23,5)]
SYNC_WAIT = 10
SPHINX_SIMULATION = False
ALGORITHM = SH_ORIGINAL
MAX_ALTITUDE=4.5
MIN_ALTITUDE=2.0
OPTIMAL_ALTITUDE=3.5
ACTIVATE_GRAPHIC_MAP = False
STREAMING_MODE_ON = True
ROTATE = False
