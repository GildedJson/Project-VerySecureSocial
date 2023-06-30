import json
import ssl
import socket

HOST, PORT = 'localhost', 8080
server = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(60)


# wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ADH-AES256-SHA")
# wrappedSocket.connect((HOST, PORT))

def send(message):
    global sock, server
    print(f'Sending: \'{message}\'')
    # wrappedSocket.send(message)
    sock.sendto(message.encode(), server)
    print('done')

    server_answer, _ = sock.recvfrom(1024)
    return server_answer.decode()
    # return wrappedSocket.recv(1280)
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
        wrappedSocket.close()
        break
