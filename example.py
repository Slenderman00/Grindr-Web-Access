#import the api
import api

tokens = api.fullLogin()
socket = api.messageSocket(tokens, onmessage)
socket.start()

print(api.getProfileId(tokens[0]))

def onmessage(tokens, message, profileid):
    print(message)



