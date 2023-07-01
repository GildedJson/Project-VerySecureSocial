import json
import socket
from cryptography.fernet import Fernet
import threading

file_enc_token = b'SoSxstZjRNRbi6JtA9yJu2RVyixvT_tWTN1jeSMq64o='
cipher_suite = Fernet(file_enc_token)

def decode_with_token(encoded_msg):
    return encoded_msg
    # return cipher_suite.decrypt(encoded_msg)

def encode_with_token(msg):
    return msg
    # return cipher_suite.encrypt(msg)

PORT = 8080
welcome_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcome_sock.bind(('', PORT))
welcome_sock.listen()


def answer_signup(username, password, all_users):
    for user in all_users['Users']:
        if user['username'] == username:
            break
    else:
        all_users['Users'].append({'username': username, 'password': password})
        with open('Users.txt', 'w') as file:
            file.write(encode_with_token(json.dumps(all_users, indent=4)))
        message = {'type': 'OK', 'message': 'Signup Successful'}
        return json.dumps(message)
    message = {'type': 'ERROR', 'message': 'Username is used'}
    return json.dumps(message)


def answer_login(username, password, all_users):
    for user in all_users['Users']:
        if user['username'] == username:
            real_password = user['password']
            break
    else:
        message = {'type': 'ERROR', 'message': 'Username not found'}
        return json.dumps(message)
    if real_password == password:
        message = {'type': 'OK', 'message': 'Login Successful'}
        online_users.append(username)
        return json.dumps(message)
    else:
        message = {'type': 'ERROR', 'message': 'Password is not correct'}
        return json.dumps(message)


def answer_exit():
    online_users


def handle_client(connection_sock):
    while True:
        command = connection_sock.recv(1024).decode()
        command_dict = json.loads(command)
        print(f'Receiving:\n{command}')

        if command_dict['type'] == 'signup':
            response = answer_signup(command_dict['username'], command_dict['password'], all_users)
        elif command_dict['type'] == 'login':
            response = answer_login(command_dict['username'], command_dict['password'], all_users)
        elif command_dict['type'] == 'online':
            response = json.dumps({'type': 'OK', 'online users': list(set(online_users))})
        elif command_dict['type'] == 'exit':
            connection_sock.close()
            answer_exit()
            break
        print(f'Sending:\n{response}')
        connection_sock.send(response.encode())
    connection_sock.close()

with open('Users.txt', 'r') as file:
    all_users = decode_with_token(json.loads(file.read()))
online_users = []

groups = None
with open('Groups.txt', 'r') as file:
    groups = json.loads(file.read())

print('Server Listening...')
while True:
    connection_sock, client = welcome_sock.accept()
    thread = threading.Thread(target=handle_client, args=(connection_sock,))
    thread.start()


