import socket
import threading

bind_ip = '172.16.138.130'
bind_port = 5900

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((bind_ip, 0))
server.listen(5)  # max backlog of connections
addr = server.getsockname()
print ('Listening: ' +str(addr[1]))
#print ('Listening {}:{}'.format(bind_ip, ))


def handle_client_connection(client_socket):
    request = client_socket.recv(1024)
    print ('Received {}'.format(request))
    client_socket.send(str.encode('ACK!'))
    client_socket.close()

while True:
    client_sock, address = server.accept()
    print ('Accepted connection from {}:{}'.format(address[0], address[1]))
    client_handler = threading.Thread(
        target=handle_client_connection,
        args=(client_sock,)
    )
    client_handler.start()
