#Simple script to explore how the new Grindr v4 web API works

import requests
import json
import terminalqr
import time
import base64
import binascii
import uuid
import threading
import xmltodict
from websocket import create_connection


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
    auth = getProfileId(authtoken) + "@chat.grindr.com" + "\00" + getProfileId(authtoken) + "\00" + authtoken
    _hex = binascii.b2a_base64(str.encode(auth), newline=False)
    _hex = str(_hex)
    _hex = _hex.replace("b'", "").replace("'", "")
    return _hex



def fullLogin():
    webClientId = fetchWebClientId()
    generateQr(webClientId)
    return [str(authtoken(webClientId)), str(webClientId)]

#
# Tring to connect to the ws-xmpp server using PLAIN SASL
#


        ##profiles = fetchProfiles(tokens[0])
        ##print("")
        ##rint("Users near you:")
        ##print("")

        #explore the data
        ##for profile in profiles["profiles"]:
        ##   print(str(profile["displayName"]) + " : " + str(profile["age"]))
        ##    print("sending: 'Halla, Hva skjer?'")
        ##    await websocket.send('<message from="' + getProfileId(tokens[0]) + '@chat.grindr.com" id="U2ot8EBFwLRAw6U9" to="' + str(profile["profileId"]) + '@chat.grindr.com" type="chat" xmlns="jabber:client"><body>{&quot;sourceProfileId&quot;:&quot;' + getProfileId(tokens[0]) + '&quot;,&quot;targetProfileId&quot;:&quot;' + str(profile["profileId"]) + '&quot;,&quot;messageId&quot;:&quot;' + str(uuid.uuid1()) + '&quot;,&quot;sourceDisplayName&quot;:&quot;200766359&quot;,&quot;type&quot;:&quot;text&quot;,&quot;timestamp&quot;:1582651816848,&quot;body&quot;:&quot;&quot;}</body></message>')
        

class messageSocket:
    def __init__(self, tokens, onmessage):
        self.ws = create_connection("wss://chat.grindr.com:2443/ws-xmpp")
        self.tokens = tokens
        self.onmessage = onmessage

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
                self.ws.send('<a h="1" xmlns="urn:xmpp:sm:3"/>')
            
            if "r xmlns" in respons: 
                i = 0

            if "failure" in respons:
                return "";

            #recieve message
        
    def messageThread(self):
        while 1:
            try:
                respons = self.ws.recv()
                respons = xmltodict.parse(respons)
                data = respons["message"]["body"]
                data = json.loads(data)
                self.onmessage(self.tokens, data["body"], data["sourceProfileId"])
            except:
                pass



    def message(self, id, message):
        data = {"sourceProfileId":str(getProfileId(self.tokens[0])),"targetProfileId":str(id),"messageId":str(uuid.uuid1()),"sourceDisplayName":str(getProfileId(self.tokens[0])),"type":"text","timestamp":1582651816848,"body":message}
        data = json.dumps(data)
        data = data.replace('"', '&quot;')
        self.ws.send('<message from="' + getProfileId(self.tokens[0]) + '@chat.grindr.com" id="U2ot8EBFwLRAw6U9" to="' + str(id) + '@chat.grindr.com" type="chat" xmlns="jabber:client"><body>' + data + '</body></message>')

    def start(self):
        self.authenticate()
        t1 = threading.Thread(target=self.messageThread)
        t1.start()
        t1.join()