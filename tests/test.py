#testing all functions
#some of the tests require user intervention

#adding folders
import sys
sys.path.append('..')
sys.path.append('../dependencies')

import api
import terminalqr

terminalqr.drawqr("Test")

web = api.fetchWebClientId()

authtoken = str(api.fullLogin())

api.fetchProfiles(authtoken)

api.fetchSettings(authtoken)

api.getProfileId(authtoken)

api.generatePlainAuth(authtoken)

token = [authtoken, web]

def onmessage(id, message):
    pass

socket = api.messageSocket(authtoken, onmessage)



