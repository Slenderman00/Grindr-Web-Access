
#imporet the api

import api

#call full login function
authtoken = api.fullLogin()

#fetch profiles
profiles = api.fetchProfiles(authtoken)
print("")
print("Users near you:")
print("")

#explore the data
for profile in profiles["profiles"]:
    print(str(profile["displayName"]) + " : " + str(profile["age"]))

print("")
print("Your profile id:")
print("")
print(api.getProfileId(authtoken))
