import json
import socket
import time
from cryptography.fernet import Fernet

# Generate random encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

rsa_public_key = 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFwca3W8bscbsDJUptQ/RpVhkwE5rxBeKUCGr0akuaIcQetXlVIiK+2wJv67+tv1VgNgIEejj/fXcUA9glnz8mfKn05EHQ9z+5ML3FjAjtA+TRvHJxqUgjOs+y06vyRe2rqd8UdsEX1f5I/IuKPQXW4joY3wrhIEDvPTA42Ib2kwIDAQAB'

HOST, PORT = 'localhost', 8080
server_address = (HOST, PORT)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# Send the encryption key to the server
client_socket.sendall(key)


# Encrypt and send messages to the server
def send(message):
    print(f'Sending:\n{message}')
    encrypted_message = cipher_suite.encrypt(message.encode())
    client_socket.sendall(encrypted_message)

    # Receive and decrypt messages from the server
    encrypted_response, _ = client_socket.recvfrom(1024)
    decrypted_response = cipher_suite.decrypt(encrypted_response)
    return decrypted_response.decode()


print('Client Starting...')
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

    elif command_parts[0] == 'msgg' and len(command_parts) >= 3:
        message_to_send = {'type': 'msgg', 'group': command_parts[1], 'msg': ' '.join(command_parts[2:]), }

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
