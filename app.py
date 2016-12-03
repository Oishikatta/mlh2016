import os
import json
import urllib
import requests
import requests_cache

from flask import Flask
from flask import render_template
from flask import request
app = Flask(__name__)

STEAM_API_KEY = ""
with open("steam_apikey.txt", mode='r') as apifile:
    STEAM_API_KEY = apifile.read().replace('\n', '')

if len(STEAM_API_KEY) != 32:
    print "Invalid Steam API key. Create steam_apikey.txt before running the app."
    exit()

requests_cache.install_cache('api_cache')


def getSteamIdFromVanityUrl(vanityUrl):
    API_CALL = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={0}&vanityurl={1}"
    response = requests.get(API_CALL.format(STEAM_API_KEY, vanityUrl)).json()
    # example response: {u'response': {u'steamid': u'76561198040673336', u'success': 1}}
    # example response: {u'response': {u'message': u'No match', u'success': 42}}

    if response['response']['success'] == 1:
        return response['response']['steamid']
    else:
        return False

def getOwnedGames(id):
    API_CALL = " http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&format=json&include_played_free_games=1&include_appinfo=1"
    response = requests.get(API_CALL.format(STEAM_API_KEY,id)).json()
    if response['response']['game_count'] > 0:
        return response['response']
    else :
        return False

@app.route("/")
def hello():
    vanityUrl = request.args.get("vanityUrl")
    if vanityUrl is None:
        return render_template("index.html")
    else:
        steamId = getSteamIdFromVanityUrl(vanityUrl)
        if steamId == False:
            return render_template("error.html", message="Invalid vanity URL.")
        else:
            data = getOwnedGames(steamId)
            return render_template("score.html", data=data)

@app.route("/git-hook", methods=['GET', 'POST'])
def githook():
    return os.popen("git pull; killall python2.7").read()

if __name__ == "__main__":
    app.run()

