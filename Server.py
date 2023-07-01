import json
import socket
from cryptography.fernet import Fernet
import threading
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

file_enc_token = b'SoSxstZjRNRbi6JtA9yJu2RVyixvT_tWTN1jeSMq64o='
cipher_suite = Fernet(file_enc_token)

rsa_private_key = '-----BEGIN RSA PRIVATE KEY-----\nMIICWgIBAAKBgGWy3cMPvRGr7rw2rKDT0uQzJBxXMZIBk8FCsSSU9Mu/Q3GqFZH+\noKIO/LX4obBzfjm2WMfvdMe6nI5+ISVXkfEeXTkVyhyvXGJvqd6F+QueQBNcC1j1\n3gUwsVtNvECSXftpx+hwr4GGNyls46dQEFCluy0W+JG1r7Q6F0kR7yfJAgMBAAEC\ngYAmN/r5FFAUdQ2p884aPqCxm7qFYAtD+I3DgkG6IrSAYWeCLs4eaJeLb6Bu7not\nKqoUHD/vG0FC0hGFx0bDls5EWOaUC06rchnouyizPcTbmVdlRgmZDcs+7hCqoZhk\nsaDbJHGfuVyCBsZR7oT02B+DEvroDU4rQT14h0/kKCQpAQJBAMA2xl5t7s04N+qW\n33bbfIZOYB6WteZ+9xkjfeEoE5XjCOL15H0RClzfNpluNFasinJxQ2nGQqh/F+0n\nj42WSiECQQCHcoOJC9g6CrEH9urTs24JqZln5Yx6yvNC3wbCZLu9nDDI+3H27AX5\nvqLqq5lxRfjLYKpc619jFJcNvtNDYTipAkArKGFT9IUI6RWNA8E7E78a/OASHi7L\niTh8GX77Hh9/qRFmvGVIO5pDDg9ZVehEicswNQQ47L4szRSXOCnAVb1hAkATqsEG\nqT2gT+UcrvGyA5+6r3Gi8GXRfp6L2y50E4RfJ8q9pCUMIYFMni2xvXDuTaaugT67\nd0HGdTrpuAedBQThAkBsgN3IhDw44N95nZHGIdSCZHsC64Q3QQ2eif5o7yWu0iSS\nEd9lJHOZORxi42Oss4Xlj9k5EQdRybDdi5jmLjSg\n-----END RSA PRIVATE KEY-----'
rsa_private_RsaKey = RSA.import_key(rsa_private_key)
rsa_decryptor = PKCS1_OAEP.new(rsa_private_RsaKey)

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


def answer_signup(username, password, all_users, current_user):
    if current_user is not None:
        message = {'type': 'ERROR', 'message': 'Exit required'}
    else:
        for user in all_users['Users']:
            if user['username'] == username:
                message = {'type': 'ERROR', 'message': 'Username is used'}
                break
        else:
            all_users['Users'].append({'username': username, 'password': password})
            with open('Users.txt', 'w') as file:
                file.write(encode_with_token(json.dumps(all_users, indent=4)))
            message = {'type': 'OK', 'message': 'Signup Successful'}
    return json.dumps(message)


def answer_login(username, password, all_users, current_user):
    if current_user is not None:
        message = {'type': 'ERROR', 'message': 'Exit required'}
    else:
        for user in all_users['Users']:
            if user['username'] == username:
                if user['password'] == password:
                    message = {'type': 'OK', 'message': 'Login Successful'}
                    current_user = username
                    online_users.append(username)
                else:
                    message = {'type': 'ERROR', 'message': 'Password is not correct'}
                break
        else:
            message = {'type': 'ERROR', 'message': 'Username not found'}
    return json.dumps(message), current_user


def handle_client(connection_sock):
    current_user = None
    while True:
        command = connection_sock.recv(1024).decode()
        command_dict = json.loads(command)
        print(f'Receiving:\n{command}')

        if command_dict['type'] == 'signup':
            response = answer_signup(command_dict['username'], command_dict['password'], all_users, current_user)
        elif command_dict['type'] == 'login':
            response, current_user = answer_login(command_dict['username'], command_dict['password'], all_users, current_user)
        elif current_user is None:
            response = json.dumps({'type': 'ERROR', 'message': 'Login required'})
        elif command_dict['type'] == 'online':
            response = json.dumps({'type': 'OK', 'online users': list(set(online_users))})
        elif command_dict['type'] == 'exit':
            online_users.remove(current_user)
            connection_sock.close()
            break
        print(f'Sending:\n{response}')
        connection_sock.send(response.encode())


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
