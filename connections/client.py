import socket
import properties
import netifaces as ni
import ipaddress
import threading
from subprocess import Popen, PIPE
from flightplans import drone
import utils
import time

#CONSTANTS
port = properties.PORT
interface = properties.INTERFACE
#bind_ip = properties.IP_DRON_1
#bind_port = 5900
net_ip = properties.IP_BASE
netmask = properties.NETMASK
ip_address = net_ip +"/" +netmask
ping_timeout = properties.PING_TIMEOUT

class client:

    def __init__(self):
        self.network = ipaddress.ip_network(ip_address)
        self.friends = []

    def check_connection(self, ip):
        toping = Popen(['ping', '-c', '1', '-w', ping_timeout, ip], stdout=PIPE)
        output = toping.communicate()[0]
        return toping.returncode


    def search_friends(self, my_ip):
        time.sleep(5)
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
            client.connect((ip_address, port))
            client.send(str.encode(msj))
            response = client.recv(4096)
            print (response)
        except:
            pass


    def send_message(self, msj):
        def send_message_thread(self, msj):
            for ip in self.friends:
                ip = str(ip)
                hostalive = self.check_connection(ip)
                if hostalive == 0:
                    print(ip, 'enviado mensaje')
                    self.client_request(ip,msj)
                else:
                    print(ip, 'no se encontro el dron')
                    handler = threading.Thread(
                        target=self.reconect,
                        args=(msj,ip)
                    )
                    handler.start()
        handler = threading.Thread(
            target=send_message_thread,
            args=(self, msj,)
        )
        handler.start



    def reconect(self, msj, ip):
        found = False
        while not found:
            time.sleep(5)
            hostalive = self.check_connection(ip)
            if hostalive == 0:
                print(ip, 'reconexion exitosa')
                self.client_request(ip,msj)
                found = True
