# import the api
import api

tokens = api.fullLogin()
print(api.getProfileId(tokens[0]))

s1 = api.settings(tokens)
s1.updateProfileSettings(aboutMe='test')

def onmessage(message, profileid, _type):
    #returns taps
    if(_type == "tap"):
        print(profileid + " tapped you. returning tap")
        socket.tap(profileid, 0)

socket = api.messageSocket(tokens, onmessage)
socket.start()



