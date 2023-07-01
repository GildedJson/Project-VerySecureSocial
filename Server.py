import json
import socket

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
            file.write(json.dumps(all_users, indent=4))
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


def answer_online():
    return json.dumps({'type': 'OK', 'online users': list(set(online_users))})


def answer_exit():
    online_users


def decode_with_token(encoded_msg):
    return encoded_msg  # TODO


def encode_with_token(msg):
    return msg  # TODO


with open('Users.txt', 'r') as file:
    all_users = json.loads(file.read())
online_users = []

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
        elif command_dict['type'] == 'login':
            response = answer_login(command_dict['username'], command_dict['password'], all_users)
        elif command_dict['type'] == 'online':
            print(online_users)
            response = answer_online()
        elif command_dict['type'] == 'exit':
            connection_sock.close()
            answer_exit()
            break
        print(f'Sending:\n{response}')
        connection_sock.send(response.encode())
    connection_sock.close()
