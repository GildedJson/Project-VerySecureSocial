import json
import socket

# create socket
PORT = 8080
welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to local port
welcome_sock.bind(('', PORT))

# server begins listening for incoming TCP requests
welcome_sock.listen()

print('Server Starting...')
while True:
    connection_sock, client = welcome_sock.accept()
    command = connection_sock.recv(1024).decode()
    command_dict = json.loads(command)
    print(f'Received Message:\n{command}')

    if command_dict['type'] == 'signup':
        response = 'sample response'
        connection_sock.send(response.encode())
