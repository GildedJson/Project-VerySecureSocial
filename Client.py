import json

def send(message):
    print(f'Sending: \'{message}\'')
    return 'OK'




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
        break

