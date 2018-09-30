from enums import SH_ORIGINAL, SH_TIMESTAMP, RANDOM

IP_BASE="172.16.138.64"
NETMASK="29"
PORT=43261
PING_TIMEOUT="1"
#INTERFACE="eth0"
INTERFACE="wlp3s0"
RANGO_LARGO=1.81
RANGO_ANCHO=1.81
MAPA_LARGO=43.44
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
POI_POSITIONS = [(23,13),(10,16),(0,6),(14,25),(6,22),(9,13),(13,19),(5,3),(13,3),(20,2),(10,10),(2,10),(5,13),(19,23),(21,20),(16,2),(18,23),(14,19),(11,9),(13,17),(3,26),(11,21),(15,0),(14,16),(10,6),(12,22),(15,17),(9,16),(7,5),(17,12),(12,7)]
POI_TIMERS = [220,276,124,228,237,248,291,277,161,255,298,159,264,209,219,193,260,201,293,160,246,150,274,160,289,145,204,221,299,283,205]
POI_CRITICO_TIMERS = [92,74,64,79,91,73,95,60,82,102,70,119,120,71,108,79,64,83,119,91,65,90,98,77,106,80,74,75,67,119,95]
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