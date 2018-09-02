import socket
from properties import SPHINX_PORT, PORT, INTERFACE, SPHINX_SIMULATION
import netifaces as ni
import threading
from threading import Lock
import json
from flightplans import drone
from stateMachine.statesEnum import FIN


class server:

    def __init__(self, bebop, stateMachine):
        self.bebop = bebop
        self.stateMachine = stateMachine
        self.endServer = False
        self.mutex = Lock()
        ip = '127.0.0.1'
        port = SPHINX_PORT
        if not SPHINX_SIMULATION:
            ip = ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr']
            port = PORT
        print ("Server IP: ", ip, port)
        self.ip = ip
        self.port = port

    def get_server_ip(self):
        return self.ip

    def run_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(5)  # max backlog of connections
        addr = server.getsockname()
        print ('Listening: ' + str(addr[1]))
        end = False

        def handle_client_connection(self, client_socket, drone, stateMachine):
            request = client_socket.recv(1024)
            print ('Received {}'.format(request))
            client_socket.send(str.encode('ACK!'))
            client_socket.close()
            received_message_str = request.decode("utf-8")
            received_message = json.loads(received_message_str)
            if(received_message["state"] == FIN):
                self.mutex.acquire()
                self.endServer = True
                self.mutex.release()
            else:
                stateMachine.handleMessage(received_message)

        while not end:
            client_sock, address = server.accept()
            print ('Accepted connection from {}:{}'.format(address[0], address[1]))
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(self, client_sock, drone, self.stateMachine,)
            )
            client_handler.start()
            self.mutex.acquire()
            end = self.endServer
            self.mutex.release()
