import json
import socket
from cryptography.fernet import Fernet
import threading
import ssl

file_enc_token = b'SoSxstZjRNRbi6JtA9yJu2RVyixvT_tWTN1jeSMq64o='
file_cipher_suite = Fernet(file_enc_token)

rsa_private_key = 'MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIXBxrdbxuxxuwMlSm1D9GlWGTATmvEF4pQIavRqS5ohxB61eVUiIr7bAm/rv62/VWA2AgR6OP99dxQD2CWfPyZ8qfTkQdD3P7kwvcWMCO0D5NG8cnGpSCM6z7LTq/JF7aup3xR2wRfV/kj8i4o9BdbiOhjfCuEgQO89MDjYhvaTAgMBAAECgYAzUcLlrQ/ovkYrkc45mB4ZoFAvswX6vfBOLeCjgHkbXSM7SRORh3RfV/ZabNBxYHzoWjBx+VcPJ9tdUZBH9w6qLDMzY/6jYjUbLzsd43bQCDaJckeqpSdBH/b3zcqdIY9VHV0rjN61cGxypwNHmcOhfuaempbOs13tIONK0sK28QJBAN6YNumi45dpgx+uJzILArMq7JHHQhkahNdwQF4bOAn7kd+++72xFmSc1ermLhgM9k8e2KP4VkgQTP1OTn97ZNkCQQCZ1InUhf2Ap7iSpB3fSK3cT7YaHQJ0B2WGfGoNXoan2+t1igUiZFoGp6gTkiHOoAu57NyBl3jaXMDDhJRUFONLAkBpKjsPaRDj8UqtBgeoogEVixsXyK9W0uueKX+PtoZkWQHTVxTyyx7MTDjY8QUoAb/BI86wsVx6UZE+P+fgXPkJAkBhX+2jjvGqWAD5KlQSfEI5/GdMXmKoKep1WBoVvmlEpmyE6cpYO+fU4Jn/UXh/AEaL+ciXa9e/egk3epweIV7DAkEAv5svnZrizKGMWMD3rm3oBD921LhjI+rfCoWY5XulnNizCfbfRrqC0U1vqEkwxGQW5okeassLdwPT9iskaC/lKw=='



def decode_with_token(encoded_msg):
    return encoded_msg
    # return cipher_suite.decrypt(encoded_msg)


def encode_with_token(msg):
    return msg
    # return cipher_suite.encrypt(msg)



def answer_signup(username, password, current_user):
    if current_user is not None:
        message = {'type': 'ERROR', 'message': 'Exit Required'}
    else:
        if exist_user(username):
            message = {'type': 'ERROR', 'message': 'Username is Used'}
        else:
            all_users['Users'].append({'username': username, 'password': password})
            with open('Users.txt', 'w') as file:
                file.write(encode_with_token(json.dumps(all_users, indent=4)))
            message = {'type': 'OK', 'message': 'Signup Successful'}
    return json.dumps(message)


def answer_login(username, password, current_user):
    if current_user is not None:
        message = {'type': 'ERROR', 'message': 'Exit Required'}
    else:
        for user in all_users['Users']:
            if user['username'] == username:
                if user['password'] == password:
                    message = {'type': 'OK', 'message': 'Login Successful'}
                    current_user = username
                    online_users.append(username)
                else:
                    message = {'type': 'ERROR', 'message': 'Password is not Correct'}
                break
        else:
            message = {'type': 'ERROR', 'message': 'Username not Found'}
    return json.dumps(message), current_user


def answer_direct(contact, direct, current_user):
    for user in all_users['Users']:
        if user['username'] == contact:
            message = {'type': 'OK', 'message': 'Direct Message Delivered'}
            all_directs.append([current_user, contact, direct])
            break
    else:
        message = {'type': 'ERROR', 'message': 'Contact not Found'}
    return json.dumps(message)


def answer_inbox(current_user):
    message = {'type': 'OK'}
    directs = []
    for direct in all_directs:
        if direct[1] == current_user:
            directs.append({'sender': direct[0], 'direct': direct[2]})
    message['directs'] = directs
    return json.dumps(message)


def answer_new_group(name, current_user):
    groups_name = list(groups.keys())
    for group in groups_name:
        if group == name:
            message = {'type': 'ERROR', 'message': 'Name is already Used'}
            break
    else:
        groups[name] = {'admin': current_user, 'members': [current_user]}
        with open('Groups.txt', 'w') as file:
            file.write(encode_with_token(json.dumps(groups, indent=4)))
        message = {'type': 'OK', 'message': 'Group Created'}
    return json.dumps(message)


def answer_add(contact, group, current_user):
    if not exist_user(contact):
        message = {'type': 'ERROR', 'message': 'Contact not Found'}
    elif group not in list(groups.keys()):
        message = {'type': 'ERROR', 'message': 'Group not Found'}
    elif groups[group]['admin'] != current_user:
        message = {'type': 'ERROR', 'message': 'Group is not Yours'}
    elif contact in groups[group]['members']:
        message = {'type': 'ERROR', 'message': 'Contact is already in Group'}
    elif contact not in online_users:
        message = {'type': 'ERROR', 'message': 'Contact is Offline'}
    else:
        groups[group]['members'].append(contact)
        with open('Groups.txt', 'w') as file:
            file.write(encode_with_token(json.dumps(groups, indent=4)))
        message = {'type': 'OK', 'message': 'Contact Added to Group'}

    return json.dumps(message)


def handle_client(connection_sock):
    current_user = None
    ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)

    # Receive the encryption key from the client
    client_key = ssl_socket.recv(32)

    while True:
        encrypted_message = ssl_socket.recv(1024)
        decrypted_message = cipher_suite.decrypt(encrypted_message)
        command = decrypted_message.decode()
        command_dict = json.loads(command)
        print(f'Receiving:\n{command}')

        response = ''

        if command_dict['type'] == 'signup':
            response = answer_signup(command_dict['username'], command_dict['password'], current_user)

        elif command_dict['type'] == 'login':
            response, current_user = answer_login(command_dict['username'], command_dict['password'], current_user)

        elif current_user is None:
            response = json.dumps({'type': 'ERROR', 'message': 'Login required'})

        elif command_dict['type'] == 'online':
            response = json.dumps({'type': 'OK', 'online users': list(set(online_users))})

        elif command_dict['type'] == 'inbox':
            response = answer_inbox(current_user)

        elif command_dict['type'] == 'direct':
            response = answer_direct(command_dict['contact'], command_dict['message'], current_user)

        elif command_dict['type'] == 'new group':
            response = answer_new_group(command_dict['name'], current_user)

        elif command_dict['type'] == 'add':
            response = answer_add(command_dict['contact'], command_dict['group'], current_user)

        elif command_dict['type'] == 'exit':
            online_users.remove(current_user)
            connection_sock.close()
            break

        print(f'Sending:\n{response}')
        connection_sock.send(response.encode())


with open('Users.txt', 'r') as file:
    all_users = decode_with_token(json.loads(file.read()))
online_users = []

with open('Groups.txt', 'r') as file:
    groups = json.loads(file.read())

# each tuple: (sender, receiver, direct message)
all_directs = []

# Generate a random encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Create a socket and wrap it with SSL/TLS
PORT = 8080
HOST = 'localhost'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (HOST, PORT)
server_socket.bind(server_address)
server_socket.listen(1)


ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')

print('Server Listening...')
while True:
    client_socket, client_address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket,))
    thread.start()
