import socket
import properties
import netifaces as ni
import threading
import json
from flightplans import drone

# CONSTANTS
port = properties.PORT
interface = properties.INTERFACE
# bind_ip = properties.IP_DRON_1
# bind_port = 5900
net_ip = properties.IP_BASE
netmask = properties.NETMASK
ip_address = net_ip + "/" + netmask
ping_timeout = properties.PING_TIMEOUT


class server:

    def __init__(self, bebop, stateMachine):
        self.bebop = bebop
        self.stateMachine = stateMachine
        self.run_server()

    def get_server_ip(self):
        ni.ifaddresses(interface)
        ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
        print ("Server IP: ", ip)
        return ip

    def run_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.get_server_ip(), port))
        server.listen(5)  # max backlog of connections
        addr = server.getsockname()
        print ('Listening: ' + str(addr[1]))

        def handle_client_connection(client_socket, drone, stateMachine):
            request = client_socket.recv(1024)
            print ('Received {}'.format(request))
            client_socket.send(str.encode('ACK!'))
            client_socket.close()
            received_message_str = request.decode("utf-8")
            received_message = json.loads(received_message_str)
            stateMachine.handleMessage(received_message)

        while True:
            client_sock, address = server.accept()
            print ('Accepted connection from {}:{}'.format(address[0], address[1]))
            client_handler = threading.Thread(
            target=handle_client_connection,
            args=(client_sock,drone,stateMachine,)
            )
            client_handler.start()
