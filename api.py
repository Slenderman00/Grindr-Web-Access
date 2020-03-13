#Simple script to explore how the new Grindr v4 web API works

import requests
import json
import sys
import terminalqr
import time
import base64
import binascii
import uuid
import threading
import xmltodict
from websocket import create_connection

# Fetching web client id
def fetchWebClientId():
    url = 'https://grindr.mobi/v4/web-clients'
    postData = {}

    x = requests.post(url, data = postData)

    data = json.loads(x.text)

    return data["webClientId"]

#fetching auth token
def authtoken(id):
    statuscode = 404

    while statuscode == 404:
        url = 'https://grindr.mobi/v4/authtokens/web/' + id
        x = requests.get(url)
        statuscode = x.status_code
        time.sleep(1)
    return json.loads(x.text)["authtoken"]
            
# generating qr code from web client id
def generateQr(id):
    print("Generating QR code")
    data = "grindrwebchat_" + id
    terminalqr.drawqr(data)
    print("url: https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=grindrwebchat_" + id)


# fetch user settings
def fetchSettings(authtoken):
    url = 'https://grindr.mobi/v4/me/prefs/settings/web'
    x = requests.get(url, headers={'authorization': 'Grindr3 ' + authtoken})
    return json.loads(x.text)

# fetching all nearby profiles
def fetchProfiles(authtoken):
    # TODO: FIGURE OUT WTF THIS IS: "u4xstq8k995m"
    url = 'https://grindr.mobi/v4/locations/u4xstq8k995m/profiles?myType=false&online=false&faceOnly=false&photoOnly=false&notRecentlyChatted=false'
    x = requests.get(url, headers={'authorization': 'Grindr3 ' + authtoken})
    return json.loads(x.text)

# extracting user profile id
def getProfileId(authtoken):
    _authtoken = authtoken.split(".")
    _authtoken = _authtoken[1]

    #adding a shit ton of padding
    for i in range(len(authtoken), 400):
        _authtoken += "="

    data = base64.b64decode(_authtoken)
    
    return json.loads(data)["profileId"]

# generating plain auth
def generatePlainAuth(authtoken):
    auth = getProfileId(authtoken) + "@chat.grindr.com" + "\00" + getProfileId(authtoken) + "\00" + authtoken
    _hex = binascii.b2a_base64(str.encode(auth), newline=False)
    _hex = str(_hex)
    _hex = _hex.replace("b'", "").replace("'", "")
    return _hex


# perforiming a full login
def fullLogin():
    webClientId = fetchWebClientId()
    generateQr(webClientId)
    return [str(authtoken(webClientId)), str(webClientId)]

# xmpp stuff (WIP)
class messageSocket:
    def __init__(self, tokens, onmessage):
        self.ws = create_connection("wss://chat.grindr.com:2443/ws-xmpp")
        self.tokens = tokens
        self.onmessage = onmessage
        self.acks = 0

    def authenticate(self):
        print('<open to="chat.grindr.com" version="1.0" xmlns="urn:ietf:params:xml:ns:xmpp-framing"/>')
        self.ws.send('<open to="chat.grindr.com" version="1.0" xmlns="urn:ietf:params:xml:ns:xmpp-framing"/>')
        i = 1;
        while i:
            #WS-XMPP STATE MACHINE
            respons = self.ws.recv()

            #print(respons + "\n-------------------------------------------------------------------------------------------------------------------")

            if "features" in respons:
                self.ws.send('<auth mechanism="PLAIN" xmlns="urn:ietf:params:xml:ns:xmpp-sasl">' + generatePlainAuth(self.tokens[0])  + '</auth>')

            if "success" in respons:
                self.ws.send('<open to="chat.grindr.com" version="1.0" xmlns="urn:ietf:params:xml:ns:xmpp-framing"/>')
                self.ws.send('<iq id="_bind_auth_2" type="set" xmlns="jabber:client"><bind xmlns="urn:ietf:params:xml:ns:xmpp-bind"><resource>' + self.tokens[1] + '_web</resource></bind></iq>')

            if "_bind_auth_2" in respons: 
                self.ws.send('<iq id="_session_auth_2" type="set" xmlns="jabber:client"><session xmlns="urn:ietf:params:xml:ns:xmpp-session"/></iq>')
                self.ws.send('<iq from="' + getProfileId(self.tokens[0]) + '@chat.grindr.com/' + self.tokens[1] + '_web" id="' + str(uuid.uuid4()) + ':carbons" type="set" xmlns="jabber:client"><enable xmlns="urn:xmpp:carbons:2"/></iq>')
                self.ws.send('<enable resume="false" xmlns="urn:xmpp:sm:3"/>')
                self.ws.send('<presence xmlns="jabber:client"/>')
                time.sleep(1)
                self.ack()

            
            if "r xmlns" in respons: 
                i = 0

            if "failure" in respons:
                return "";

            #recieve message

    def ack(self):
        #to avoid getting kicked for to many unacked messages
        self.acks += 1
        self.ws.send('<a h="' + str(self.acks) + '" xmlns="urn:xmpp:sm:3"/>')

        
    def messageThread(self):
        i = 2
        while 1:
            respons = self.ws.recv()
            if respons:
                respons = xmltodict.parse(respons)
                if next(iter(respons)) == 'message':
                    self.ack()
                    try:
                        data = respons["message"]["body"]
                        data = json.loads(data)
                        if(data["type"] == "image"):
                            #generating image url
                            body = json.loads(data["body"])
                            imageUrl = "https://cdns.grindr.com/grindr/chat/" + body["imageHash"]

                            if("taps" in body["imageHash"]):
                                self.onmessage(imageUrl, data["sourceProfileId"], "tap")
                            else:
                                self.onmessage(imageUrl, data["sourceProfileId"], data["type"])
                        else:
                            self.onmessage(data["body"], data["sourceProfileId"], data["type"])
                        
                    except:
                        pass
                if next(iter(respons)) == 'presence':
                    self.ack()



    def message(self, id, message):
        data = {"sourceProfileId":str(getProfileId(self.tokens[0])),"targetProfileId":str(id),"messageId":str(uuid.uuid1()),"sourceDisplayName":str(getProfileId(self.tokens[0])),"type":"text","timestamp":time.time(),"body":str(message)}
        data = json.dumps(data)
        data = data.replace('"', '&quot;')
        self.ws.send('<message from="' + getProfileId(self.tokens[0]) + '@chat.grindr.com" id="U2ot8EBFwLRAw6U9" to="' + str(id) + '@chat.grindr.com" type="chat" xmlns="jabber:client"><body>' + data + '</body></message>')

    def tap(self, id, tapType):
        body = '{\"imageHash\":\"taps/friendly.png\",\"imageType\":2,\"tapType\":0}'
        if tapType == 1:
            body = '{\"imageHash\":\"taps/hot.png\",\"imageType\":2,\"tapType\":1}'
        if tapType == 1:
            body = '{\"imageHash\":\"taps/looking.png\",\"imageType\":2,\"tapType\":2}'

        data = {"sourceProfileId":str(getProfileId(self.tokens[0])),"targetProfileId":str(id),"messageId":str(uuid.uuid1()),"sourceDisplayName":str(getProfileId(self.tokens[0])),"type":"image","timestamp":time.time(),"body":str(body)}
        data = json.dumps(data)
        data = data.replace('"', '&quot;')
        self.ws.send('<message from="' + getProfileId(self.tokens[0]) + '@chat.grindr.com" id="U2ot8EBFwLRAw6U9" to="' + str(id) + '@chat.grindr.com" type="image" xmlns="jabber:client"><body>' + data + '</body></message>')

    def start(self):
        self.authenticate()
        self.messageThread()