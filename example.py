# import the api
import api

tokens = api.fullLogin()
print(api.getProfileId(tokens[0]))

def onmessage(message, profileid, _type):
    #returns taps
    if(_type == "tap"):
        print(profileid + " tapped you. returning tap")
        socket.tap(profileid, 0)

socket = api.messageSocket(tokens, onmessage)
socket.start()



