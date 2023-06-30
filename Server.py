import json
import socket

# create socket
PORT = 8080
welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to local port
welcome_sock.bind(('', PORT))

# server begins listening for incoming TCP requests
welcome_sock.listen()

def answer(sender, message):
    pass

def decode_with_token(encoded_msg):
    return encoded_msg #TODO

def encode_with_token(msg):
    return msg #TODO

print('Server Starting...')
groups = None
with open('GroupData.txt', 'r') as group_data_file:
    groups = json.loads(group_data_file.read())


print('Server Listening...')
while True:
    connection_sock, client = welcome_sock.accept()
    command = connection_sock.recv(1024).decode()
    command_dict = json.loads(command)
    print(f'Received Message:\n{command}')

    if command_dict['type'] == 'signup':
        response = 'sample response'
        connection_sock.send(response.encode())
