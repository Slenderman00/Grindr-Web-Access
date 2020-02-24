import api
import terminalqr

terminalqr.drawqr("Test")

api.fetchWebClientId()

authtoken = api.fullLogin()

api.fetchProfiles(authtoken)

api.fetchSettings(authtoken)

api.getProfileId(authtoken)

api.generatePlainAuth(authtoken)




