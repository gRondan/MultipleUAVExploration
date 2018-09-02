import socket
from properties import PORT, INTERFACE, IP_BASE, NETMASK, PING_TIMEOUT, SPHINX_FRIENDS, SPHINX_SIMULATION, SPHINX_PORT
import ipaddress
import threading
from subprocess import Popen, PIPE
import time
import json

# CONSTANTS
port = SPHINX_PORT
net_ip = '127.0.0.0'
if not SPHINX_SIMULATION:
    port = PORT
    net_ip = IP_BASE
interface = INTERFACE
netmask = NETMASK
ip_address = net_ip + "/" + netmask
ping_timeout = PING_TIMEOUT


class client:

    def __init__(self):
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
        for ip in self.friends:
            status = self.check_connection(ip)
            if status == 0:
                cont.append(ip)
        return cont

    def search_friends(self, my_ip):
        time.sleep(5)
        if SPHINX_SIMULATION:
            print('friend ports: ', SPHINX_FRIENDS)
            self.friends = SPHINX_FRIENDS
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
                    else:
                        print(i, 'is unreachable')

    def client_request(self, ip_address, msj):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if SPHINX_SIMULATION:
                client.connect(('127.0.0.1', ip_address))
            else:
                client.connect((ip_address, port))
            client.send(str.encode(msj))
            response = client.recv(4096)
            print (response)
        except:
            pass

    def send_message(self, msj):
        def send_message_thread(self, msj_dict):
            msj = json.dumps(msj_dict)
            for ip in self.friends:
                ip = str(ip)
                hostalive = self.check_connection(ip)
                if hostalive == 0:
                    print(ip, 'enviado mensaje')
                    self.client_request(ip, msj)
                else:
                    print(ip, 'no se encontro el dron')
                    handler = threading.Thread(
                        target=self.reconect,
                        args=(msj, ip,)
                    )
                    handler.start()
        handler = threading.Thread(
            target=send_message_thread,
            args=(self, msj,)
        )
        handler.start

    def send_direct_message(self, msj, ip):
        def send_message_thread(self, msj_dict, ip):
            msj = json.dumps(msj_dict)
            ip = str(ip)
            hostalive = self.check_connection(ip)
            if hostalive == 0:
                print(ip, 'enviado mensaje')
                self.client_request(ip, msj)
            else:
                print(ip, 'no se encontro el dron')
                handler = threading.Thread(
                    target=self.reconect,
                    args=(msj, ip,)
                )
                handler.start()
        handler = threading.Thread(
            target=send_message_thread,
            args=(self, msj, ip,)
        )
        handler.start

    def reconect(self, msj, ip):
        found = False
        while not found:
            time.sleep(5)
            hostalive = self.check_connection(ip)
            if hostalive == 0:
                print(ip, 'reconexion exitosa')
                self.client_request(ip, msj)
                found = True
