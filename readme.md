[![Build Status](https://travis-ci.com/Slenderman00/Grindr-Web-Access.svg?branch=experimental)](https://travis-ci.com/Slenderman00/Grindr-Web-Access)
[![contributors](https://img.shields.io/github/contributors/slenderman00/grindr-web-access.svg)](https://github.com/Slenderman00/Grindr-Web-Access/graphs/contributors)

# GRINDR WEB ACCESS - EXPERIMENTAL

Grindr web access is a framework for the new grindr v4 api
![](https://i.imgur.com/6SGvLxS.png)
Just scan the qrcode using your grindr app

## Installation
For easy installation using pip3 goto:
<https://github.com/Slenderman00/Pip-Grindr-Web-Access>

## Usage

```python
# import the api
import api

#api full login
tokens = api.fullLogin()
print(api.getProfileId(tokens[0]))

#on message
def onmessage(message, profileid, _type):

    #type: text, image, tap

    #do stuff with message
    print(_type + " " + message)

#open socket
socket = api.messageSocket(tokens, onmessage)
socket.start()
```

## Usage 2
```python

#fetch your own userid
api.getProfileId(tokens[0])

#send message
socket.message("<Userid>", "<Message body>")

#send tap
socket.tap("<Userid>", "<tapType>")
#tap type = 0, 1, 2
#0 = Friendly
#1 = Hot
#2 = Looking

#fetch array of all users
#                  authtoken    lat         long        parameters
api.fetchProfiles(tokens[0], 40.785091, -73.968285) # myType='false', online='false', faceOnly='false', photoOnly='false', notRecentlyChatted='false'

```

## Fetching and updating profile setting
```python
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
#closer documentation will follow

s1.displayName = "Name"
s1.aboutMe = "Test"

s1.updateProfileSettings()
```

## Todo
- add search filters

## Dependencies
- requests==2.23.0
- asyncio==3.4.3
- pyqrcode==1.2.1
- websocket_client==0.57.0
- xmltodict==0.12.0
- pygeohash==1.2.0


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)