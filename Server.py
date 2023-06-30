import json

def receive():
    pass

while True:
    sender, command = receive()
    commandDict = json.loads(command)
    if commandDict['type'] == 'signup':
        pass