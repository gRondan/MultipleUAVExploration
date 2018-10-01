import socket
from properties import PORT, INTERFACE, SPHINX_SIMULATION
from pyparrot.networking.connectionProperties import SPHINX_PORT
import netifaces as ni
import threading
from threading import Lock
import json
from flightplans import drone
from stateMachine.statesEnum import FIN


class server:

    def __init__(self, bebop, stateMachine):
        print("####################init server################")
        self.bebop = bebop
        self.stateMachine = stateMachine
        self.endServer = False
        self.mutex = Lock()
        ip = ni.ifaddresses(INTERFACE)[ni.AF_INET][0]['addr']
        port = SPHINX_PORT
        if not SPHINX_SIMULATION:
            port = PORT
        print("Server IP: ", ip, port)
        self.ip = ip
        self.port = port

    def get_server_ip(self):
        # if SPHINX_SIMULATION:
        #     return self.port
        # else:
        return self.ip

    def get_server_port(self):
        return self.port

    def run_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(5)  # max backlog of connections
        addr = server.getsockname()
        end = False

        def handle_client_connection(self, client_socket, drone, stateMachine):
            request = client_socket.recv(1024)
            client_socket.send(str.encode('ACK!'))
            client_socket.close()
            received_message_str = request.decode("utf-8")
            received_message = json.loads(received_message_str)
            print(received_message)
            if(received_message["state"] == FIN):
                self.mutex.acquire()
                self.endServer = True
                self.mutex.release()
            else:
                stateMachine.handleMessage(received_message)

        while not end:
            client_sock, address = server.accept()
            client_handler = threading.Thread(
                target=handle_client_connection,
                args=(self, client_sock, drone, self.stateMachine,)
            )
            client_handler.start()
            self.mutex.acquire()
            end = self.endServer
            self.mutex.release()
        print('TERMINO SERVER')
