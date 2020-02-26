#import the api
import api

tokens = api.fullLogin()
print(api.getProfileId(tokens[0]))

def onmessage(message, profileid):
    print(message)

socket = api.messageSocket(tokens, onmessage)
socket.start()



