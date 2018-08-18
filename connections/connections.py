import socket
import properties
import netifaces as ni
import ipaddress
import threading
from subprocess import Popen, PIPE
from flightplans import drone
import utils

#CONSTANTS
port = properties.PORT
interface = properties.INTERFACE
#bind_ip = properties.IP_DRON_1
#bind_port = 5900
net_ip = properties.IP_BASE
netmask = properties.NETMASK
ip_address = net_ip +"/" +netmask
ping_timeout = properties.PING_TIMEOUT

def client_request(ip_address, msj):
    try:
        # create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect the client
        # client.connect((target, port))
        client.connect((ip_address, port))
        # send some data (in this case a HTTP GET request)

        client.send(str.encode(msj))
        # receive the response data (4096 is recommended buffer size)
        response = client.recv(4096)

        print (response)
    except:
        pass

def get_server_ip():
    ni.ifaddresses(interface)
    ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    print ("Server IP: ", ip)
    return ip

def run_server(ip, drone):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)  # max backlog of connections
    addr = server.getsockname()
    print ('Listening: ' +str(addr[1]))
    #print ('Listening {}:{}'.format(bind_ip, ))


    def handle_client_connection(client_socket, drone):
        request = client_socket.recv(1024)
        print ('Received {}'.format(request))
        client_socket.send(str.encode('ACK!'))
        client_socket.close()
        drone.updateSearchMap(utils.convertStringToTuple(request.decode("utf-8")))


    while True:
        client_sock, address = server.accept()
        print ('Accepted connection from {}:{}'.format(address[0], address[1]))
        client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,drone,)
        )
        client_handler.start()

def send_message(msj):
    network = ipaddress.ip_network(ip_address)
    for i in network.hosts():
    	i = str(i)
    	toping = Popen(['ping', '-c', '1', '-w', ping_timeout, i], stdout=PIPE)
    	output = toping.communicate()[0]
    	hostalive = toping.returncode
    	if hostalive == 0:
    		print(i, 'IS REACHABLE')
    		client_request(i,msj)
    	else:
    		print(i, 'is unreachable')
