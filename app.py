import os
import json
import urllib

from flask import Flask
from flask import render_template

app = Flask(__name__)

STEAM_API_KEY = ""
with open("steam_apikey.txt", mode='r') as apifile:
    STEAM_API_KEY = apifile.read().replace('\n', '')

if len(STEAM_API_KEY) != 32:
    print "Invalid Steam API key. Create steam_apikey.txt before running the app."
    exit()

def getSteamIdFromVanityUrl(vanityUrl):
    API_CALL = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={0}&vanityurl={1}"
    url = urllib.urlopen(API_CALL.format(STEAM_API_KEY, vanityUrl)).read()
    response = json.loads(url)
    # example response: {u'response': {u'steamid': u'76561198040673336', u'success': 1}}
    # example response: {u'response': {u'message': u'No match', u'success': 42}}

    if response['response']['success'] == 1:
        return response['response']['steamid']
    else:
        return False

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/git-hook", methods=['GET', 'POST'])
def githook():
    return os.popen("git pull; killall python2.7").read()

if __name__ == "__main__":
    app.run()

