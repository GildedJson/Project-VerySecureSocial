import json
import socket
from cryptography.fernet import Fernet
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

rsa_public_key = '-----BEGIN PUBLIC KEY-----\nMIGeMA0GCSqGSIb3DQEBAQUAA4GMADCBiAKBgGWy3cMPvRGr7rw2rKDT0uQzJBxX\nMZIBk8FCsSSU9Mu/Q3GqFZH+oKIO/LX4obBzfjm2WMfvdMe6nI5+ISVXkfEeXTkV\nyhyvXGJvqd6F+QueQBNcC1j13gUwsVtNvECSXftpx+hwr4GGNyls46dQEFCluy0W\n+JG1r7Q6F0kR7yfJAgMBAAE=\n-----END PUBLIC KEY-----'
rsa_public_RsaKey = RSA.import_key(rsa_public_key)
rsa_encryptor = PKCS1_OAEP.new(rsa_public_RsaKey)

HOST, PORT = 'localhost', 8080
server_address = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

session_key = Fernet.generate_key()
cipher_suite = Fernet(session_key)
encrypted_session_key = rsa_encryptor.encrypt(session_key)


# Encrypt and send messages to the server
def send(message):
    print(f'Sending:\n{message}')
    # encrypted_message = cipher_suite.encrypt(message.encode())
    encrypted_message = message.encode()
    client_socket.send(encrypted_message)

    # Receive and decrypt messages from the server
    encrypted_response, _ = client_socket.recvfrom(1024)
    # decrypted_response = cipher_suite.decrypt(encrypted_response)
    decrypted_response = encrypted_response
    return decrypted_response.decode()


print('Client Starting...')

# client_socket.send(session_key)
# response, _ = client_socket.recvfrom(1024)
# time_stamp = time.time()
# client_socket.send(cipher_suite.encrypt(time_stamp))

while True:
    command = input().lower()
    command_parts = command.split(' ')
    if command_parts[0] == 'signup' and len(command_parts) == 3:
        message_to_send = {'type': 'signup', 'username': command_parts[1], 'password': command_parts[2], }

    elif command_parts[0] == 'login' and len(command_parts) == 3:
        message_to_send = {'type': 'login', 'username': command_parts[1], 'password': command_parts[2], }

    elif command_parts[0] == 'online' and len(command_parts) == 1:
        message_to_send = {'type': 'online', }

    elif command_parts[0] == 'inbox' and len(command_parts) == 1:
        message_to_send = {'type': 'inbox'}

    elif command_parts[0] == 'new_group' and len(command_parts) == 2:
        message_to_send = {'type': 'new group', 'name': command_parts[1], }

    elif command_parts[0] == 'add' and len(command_parts) == 3:
        message_to_send = {'type': 'add', 'contact': command_parts[1], 'group': command_parts[2]}

    elif command_parts[0] == 'broadcast' and len(command_parts) >= 3:
        message_to_send = {'type': 'broadcast', 'group': command_parts[1], 'message': ' '.join(command_parts[2:]), }

    elif command_parts[0] == 'direct' and len(command_parts) >= 3:
        message_to_send = {'type': 'direct', 'contact': command_parts[1], 'message': ' '.join(command_parts[2:]), }

    elif command_parts[0] == 'exit' and len(command_parts) == 1:
        message_to_send = {'type': 'exit'}

    else:
        print('Invalid Command')
        continue

    answer = send(json.dumps(message_to_send))
    print(f'Receiving:\n{answer}')

    if command_parts[0] == 'exit':
        client_socket.close()
        break
