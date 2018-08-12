import socket

hostname, sld, tld, port = 'www', 'integralist', 'co.uk', 80
target = '{}.{}.{}'.format(hostname, sld, tld)

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
# client.connect((target, port))
client.connect(('172.16.138.183', 43261))

# send some data (in this case a HTTP GET request)
msj = 'Hello'
client.send(str.encode(msj))

# receive the response data (4096 is recommended buffer size)
response = client.recv(4096)

print (response)
