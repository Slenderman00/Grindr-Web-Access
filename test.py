#testing all functions
#some of the tests require user intervention
import api
import terminalqr

terminalqr.drawqr("Test")

web = api.fetchWebClientId()

authtoken = str(api.fullLogin())

#Geohash: Pls, take a look on Wikipedia, pretty interesting info about it.
#In order to request profiles around a given location, you need to give a geohash (encoded coordinates) which is what you asked WTF it was haha
#Look geohash.co for converting latitude and longitude to geohash
# "u09tunqu9m7m" is the location for the Eiffel Tower in Paris. 
# TODO: Implement a latitude longitude to geohash converter.
geohash = 'u09tunqu9m7m'

api.fetchProfiles(authtoken, geohash)

api.fetchSettings(authtoken)

api.getProfileId(authtoken)

api.generatePlainAuth(authtoken)

token = [authtoken, web]

def onmessage(message, id, _type):
    pass

socket = api.messageSocket(authtoken, onmessage)



