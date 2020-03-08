# import the api
import api

tokens = api.fullLogin()
print(api.getProfileId(tokens[0]))

def onmessage(message, profileid, _type):
    print(_type + " " + message)

socket = api.messageSocket(tokens, onmessage)
socket.start()



