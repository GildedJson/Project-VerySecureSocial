import json
import socket
from cryptography.fernet import Fernet

file_enc_token = b'SoSxstZjRNRbi6JtA9yJu2RVyixvT_tWTN1jeSMq64o='
cipher_suite = Fernet(file_enc_token)

def decode_with_token(encoded_msg):
    return encoded_msg
    # return cipher_suite.decrypt(encoded_msg)

def encode_with_token(msg):
    return msg
    # return cipher_suite.encrypt(msg)


# create socket
PORT = 8080
welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind socket to local port
welcome_sock.bind(('', PORT))

# server begins listening for incoming TCP requests
welcome_sock.listen()


def answer_signup(username, password, all_users):
    for user in all_users['Users']:
        if user['username'] == username:
            break
    else:
        all_users['Users'].append({'username': username, 'password': password})
        with open('Users.txt', 'w') as file:
            file.write(encode_with_token(json.dumps(all_users, indent=4)))
        message = {
            'type': 'OK',
            'message': 'Signup Successful'
        }
        return json.dumps(message)
    message = {
        'type': 'ERROR',
        'message': 'Username is used'
    }
    return json.dumps(message)



users = None
with open('Users.txt', 'r') as file:
    all_users = decode_with_token(json.loads(file.read()))

groups = None
with open('Groups.txt', 'r') as file:
    groups = json.loads(file.read())

print('Server Listening...')
while True:
    connection_sock, client = welcome_sock.accept()
    while True:
        command = connection_sock.recv(1024).decode()
        command_dict = json.loads(command)
        print(f'Receiving:\n{command}')

        if command_dict['type'] == 'signup':
            response = answer_signup(command_dict['username'], command_dict['password'], all_users)

        connection_sock.send(response.encode())
