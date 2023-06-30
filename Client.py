import json
import socket

HOST, PORT = 'localhost', 8080
server = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server)


def send(message):
    global sock, server
    print(f'Sending: \'{message}\'')
    sock.send(message.encode())
    response, _ = sock.recvfrom(1024)
    return response.decode()
    # return 'OK'


print('Client Starting...')
while True:
    command = input().lower()
    commandParts = command.split(' ')
    if commandParts[0] == 'signup' and len(commandParts) == 3:
        messageToSend = {
            'type': 'signup',
            'username': commandParts[1],
            'password': commandParts[2],
        }
        answer = send(json.dumps(messageToSend))
        print(answer)
    elif commandParts[0] == 'login' and len(commandParts) == 3:
        messageToSend = {
            'type': 'login',
            'username': commandParts[1],
            'password': commandParts[2],
        }
        answer = send(json.dumps(messageToSend))
        print(answer)
    elif commandParts[0] == 'online' and len(commandParts) == 1:
        messageToSend = {
            'type': 'online',
        }
        answer = send(json.dumps(messageToSend))
        print(answer)
    elif commandParts[0] == 'newgroup' and len(commandParts) == 2:
        messageToSend = {
            'type': 'online',
            'name': commandParts[1],
        }
        answer = send(json.dumps(messageToSend))
        print(answer)
    elif commandParts[0] == 'msgg' and len(commandParts) >= 3:
        messageToSend = {
            'type': 'msgg',
            'group': commandParts[1],
            'msg': ' '.join(commandParts[2:]),
        }
        answer = send(json.dumps(messageToSend))
        print(answer)
    elif commandParts[0] == 'msgd' and len(commandParts) >= 3:
        messageToSend = {
            'type': 'msgg',
            'contact': commandParts[1],
            'msg': ' '.join(commandParts[2:]),
        }
        answer = send(json.dumps(messageToSend))
        print(answer)
    elif commandParts[0] == 'exit':
        wrap_sock.close()
        break
