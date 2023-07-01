import json
import socket
import time

HOST, PORT = 'localhost', 8080
server = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server)


def send(message):
    print(f'Sending:\n{message}')
    sock.send(message.encode())
    response, _ = sock.recvfrom(1024)
    return response.decode()


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

    elif command_parts[0] == 'newgroup' and len(command_parts) == 2:
        message_to_send = {'type': 'online', 'name': command_parts[1], }

    elif command_parts[0] == 'msgg' and len(command_parts) >= 3:
        message_to_send = {'type': 'msgg', 'group': command_parts[1], 'msg': ' '.join(command_parts[2:]), }

    elif command_parts[0] == 'msgd' and len(command_parts) >= 3:
        message_to_send = {'type': 'msgg', 'contact': command_parts[1], 'msg': ' '.join(command_parts[2:]), }
    elif command_parts[0] == 'exit' and len(command_parts) == 1:
        message_to_send = {'type': 'exit'}
    answer = send(json.dumps(message_to_send))
    print(f'Receiving:\n{answer}')

    if command_parts[0] == 'exit':
        sock.close()
        break
