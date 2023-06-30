import json
import socket

# create socket
PORT = 8080
sock = socket.socket(AF_INET, SOCK_DGRAM)

# bind socket to local port
sock.bind(('', PORT))

print('Server Starting...')
while True:
    command, sender = sock.recvfrom(1024)
    command_dict = json.loads(command.decode())

    if command_dict['type'] == 'signup':
        response = 'sample'
        sock.sendto(response.encode(), sender)
