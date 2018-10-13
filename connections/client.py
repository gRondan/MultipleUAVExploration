import socket
from properties import PORT, INTERFACE, IP_BASE, NETMASK, PING_TIMEOUT, SPHINX_SIMULATION
from pyparrot.networking.connectionProperties import SPHINX_FRIENDS_IP, SPHINX_PORT, SPHINX_FRIENDS_PORTS
import ipaddress
import threading
from subprocess import Popen, PIPE
import time
import json

# CONSTANTS
port = SPHINX_PORT
net_ip = '127.0.0.1'
if not SPHINX_SIMULATION:
    # port = PORT
    net_ip = IP_BASE
interface = INTERFACE
netmask = NETMASK
ip_address = net_ip + "/" + netmask
ping_timeout = PING_TIMEOUT


class client:

    def __init__(self):
        if SPHINX_SIMULATION is not True:
            self.network = ipaddress.ip_network(ip_address)
        self.friends = []

    def check_connection(self, ip):
        # Cambiar si se quiere simular la falta de conexion en sphinx
        if SPHINX_SIMULATION:
            return 0
        toping = Popen(['ping', '-c', '1', '-w', ping_timeout, ip], stdout=PIPE)
        output = toping.communicate()[0]
        return toping.returncode

    def check_friends(self):
        cont = []
        currentPosition = 0
        for ip in self.friends:
            print("ip: ", ip)
            status = self.check_connection(ip)
            if status == 0:
                cont.append(dict({"ip": ip, "port": self.friendsPorts[currentPosition]}))
            currentPosition += 1
        return cont

    def search_friends(self, my_ip):
        time.sleep(5)
        if SPHINX_SIMULATION:
            self.friends = SPHINX_FRIENDS_IP
            self.friendsPorts = SPHINX_FRIENDS_PORTS
        else:
            for i in self.network.hosts():
                i = str(i)
                if(i != my_ip):
                    toping = Popen(['ping', '-c', '1', '-w', ping_timeout, i], stdout=PIPE)
                    output = toping.communicate()[0]
                    hostalive = toping.returncode
                    if hostalive == 0:
                        print(i, 'IS REACHABLE')
                        self.friends.append(i)
                        self.friendsPorts.append(PORT)
                    else:
                        print(i, 'is unreachable')

    def client_request(self, ip_address, port, msj):
        # try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # if SPHINX_SIMULATION:
        #     client.connect(('127.0.0.1', int(ip_address)))
        # else:
        client.connect((ip_address, port))
        client.send(str.encode(msj))
        response = client.recv(4096)
        print(response)
        # except:
        #     pass

    def send_message(self, msj):
        def send_message_thread(self, msj_dict):
            msj = json.dumps(msj_dict)
            currentPosition = 0
            for ip in self.friends:
                port = self.friendsPorts[currentPosition]
                currentPosition += 1
                ip = str(ip)
                hostalive = self.check_connection(ip)
                if hostalive == 0:
                    try:
                        self.client_request(ip, port, msj)
                    except ConnectionRefusedError as err:
                        print("ConnectionRefusedError error: Unable to send message to {}".format(ip))
                else:
                    print(ip, 'no se encontro el dron')
                    handler = threading.Thread(
                        target=self.reconect,
                        args=(msj, ip, port,)
                    )
                    handler.start()
        handler = threading.Thread(
            target=send_message_thread,
            args=(self, msj,)
        )
        handler.start()

    def send_direct_message(self, msj, ip, port=PORT):
        def send_message_thread(self, msj_dict, ip, port):
            msj = json.dumps(msj_dict)
            ip = str(ip)
            hostalive = self.check_connection(ip)
            if hostalive == 0:
                try:
                    self.client_request(ip, port, msj)
                except ConnectionRefusedError as err:
                    print("ConnectionRefusedError error: Unable to send message to {}:{}".format(ip, port))
            else:
                print(ip, 'no se encontro el dron')
                handler = threading.Thread(
                    target=self.reconect,
                    args=(msj, ip, port)
                )
                handler.start()
        handler = threading.Thread(
            target=send_message_thread,
            args=(self, msj, ip, port,)
        )
        handler.start()

    def reconect(self, msj, ip, port):
        found = False
        while not found:
            time.sleep(5)
            hostalive = self.check_connection(ip)
            if hostalive == 0:
                print(ip, 'reconexion exitosa')
                self.client_request(ip, port, msj)
                found = True
