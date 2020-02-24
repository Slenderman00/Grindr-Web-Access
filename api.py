#Simple script to explore how the new Grindr v4 web API works

import requests
import json
import terminalqr
import time
import base64
import websockets
import asyncio
import binascii

def fetchWebClientId():
    url = 'https://grindr.mobi/v4/web-clients'
    postData = {}

    x = requests.post(url, data = postData)

    data = json.loads(x.text)

    return data["webClientId"]

def authtoken(id):
    statuscode = 404

    while statuscode == 404:
        url = 'https://grindr.mobi/v4/authtokens/web/' + id
        x = requests.get(url)
        statuscode = x.status_code
        time.sleep(1)
    print("Login sucsessfull grindr API returned: " + json.loads(x.text)["authtoken"])
    return json.loads(x.text)["authtoken"]
            
def generateQr(id):
    print("Generating QR code")
    data = "grindrwebchat_" + id
    terminalqr.drawqr(data)
    print("url: https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=grindrwebchat_" + id)

def fetchSettings(authtoken):
    url = 'https://grindr.mobi/v4/me/prefs/settings/web'
    x = requests.get(url, headers={'authorization': 'Grindr3 ' + authtoken})
    return json.loads(x.text)

def fetchProfiles(authtoken):
    url = 'https://grindr.mobi/v4/locations/u4xstq8k995m/profiles?myType=false&online=false&faceOnly=false&photoOnly=false&notRecentlyChatted=false'
    x = requests.get(url, headers={'authorization': 'Grindr3 ' + authtoken})
    return json.loads(x.text)

def getProfileId(authtoken):
    _authtoken = authtoken.split(".")
    _authtoken = _authtoken[1]

    #adding a shit ton of padding
    for i in range(len(authtoken), 400):
        _authtoken += "="

    data = base64.b64decode(_authtoken)
    
    return json.loads(data)["profileId"]

def generatePlainAuth(authtoken):
    auth = getProfileId(authtoken) + "@chat.grindr.com." + getProfileId(authtoken) + "." + authtoken
    i = 1
    _auth = ""
    for char in auth:
        if i == 24:
            char = char + "\n"
            i = 0
        _auth += char
        i += 1

    #print(_auth)
    _hex = binascii.b2a_base64(str.encode(_auth), newline=False)
    _hex = str(_hex)
    _hex = _hex.replace("b'", "").replace("'", "")
    return _hex



def fullLogin():
    webClientId = fetchWebClientId()
    generateQr(webClientId)
    return authtoken(webClientId)

#
# Tring to connect to the ws-xmpp server using PLAIN SASL
#

async def getId():
    uri = "wss://chat.grindr.com:2443/ws-xmpp"
    async with websockets.connect(uri) as websocket:
        print('<open to="chat.grindr.com" version="1.0" xmlns="urn:ietf:params:xml:ns:xmpp-framing"/>')
        await websocket.send('<open to="chat.grindr.com" version="1.0" xmlns="urn:ietf:params:xml:ns:xmpp-framing"/>')
        while 1:
            #WS-XMPP STATE MACHINE
            respons = await websocket.recv()

            print(respons)

            if "features" in respons:
                print('<auth mechanism="PLAIN" xmlns="urn:ietf:params:xml:ns:xmpp-sasl">' + generatePlainAuth(authtoken)  + '</auth>')
                await websocket.send('<auth mechanism="PLAIN" xmlns="urn:ietf:params:xml:ns:xmpp-sasl">' + generatePlainAuth(authtoken)  + '</auth>')

            if "success" in respons:
                print("succsess")
                await websocket.send('<open to="chat.grindr.com" version="1.0" xmlns="urn:ietf:params:xml:ns:xmpp-framing"/>')
                await websocket.send('<iq id="_bind_auth_2" type="set" xmlns="jabber:client"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"><resource>' + fetchWebClientId() + '_web</resource></bind></iq>')

            if "failure" in respons:
                return "";

#asyncio.get_event_loop().run_until_complete(getId())
