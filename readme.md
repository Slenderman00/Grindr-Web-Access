[![Build Status](https://travis-ci.com/Slenderman00/Grindr-Web-Access.svg?branch=master)](https://travis-ci.com/Slenderman00/Grindr-Web-Access)

# GRINDR WEB ACCESS

Grindr web access is a framework for the new grindr v4 api
![](https://i.imgur.com/6SGvLxS.png)
Just scan the qrcode using your grindr app

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

#fetch array of all users
api.fetchProfiles(tokens[0])

```

## Todo
- add search filters

## Dependencies
- requests==2.23.0
- asyncio==3.4.3
- pyqrcode==1.2.1
- websocket_client==0.57.0
- xmltodict==0.12.0


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)