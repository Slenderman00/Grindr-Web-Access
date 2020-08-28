# import the api
import api

tokens = api.fullLogin()
print(api.getProfileId(tokens[0]))

#fetch profile settings
s1 = api.settings(tokens)
print(s1.displayName)
print(s1.aboutMe)
print(s1.age)
print(s1.showAge)
print(s1.ethnicity)
print(s1.relationshipStatus)
print(s1.grindrTribes)
print(s1.lookingFor)
print(s1.bodyType)
print(s1.sexualPosition)
print(s1.hivStatus)
print(s1.lastTestedDate)
print(s1.height)
print(s1.weight)
print(s1.socialNetworks)
print(s1.showDistance)
print(s1.meetAt)
print(s1.nsfw)

#all these parameters can now be changed
#documentation will follow

s1.displayName = "Name"
s1.aboutMe = "Test"

s1.updateProfileSettings()

def onmessage(message, profileid, _type):
    #returns taps
    if(_type == "tap"):
        print(profileid + " tapped you. returning tap")
        socket.tap(profileid, 0)

#socket = api.messageSocket(tokens, onmessage)
#socket.start()



