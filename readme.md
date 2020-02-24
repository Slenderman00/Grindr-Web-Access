[![Build Status](https://travis-ci.com/Slenderman00/Grindr-Web-Accsess.svg?branch=master)](https://travis-ci.com/Slenderman00/Grindr-Web-Accsess)

# GRINDR WEB ACCSESS

Grindr web accsess is a framework for the new grindr v4 api
![](https://i.imgur.com/6SGvLxS.png)

## Usage

```python

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

#fetch your own profile id

print(api.getProfileId(authtoken))

```

## Dependencies
- requests
- json
- terminalqr
- time
- base64
- websockets
- asyncio
- binascii


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)