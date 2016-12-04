import os
import json
import urllib
import requests
import requests_cache
from collections import OrderedDict

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
    with requests_cache.disabled():
        response = requests.get(API_CALL.format(STEAM_API_KEY, vanityUrl)).json()
        # example response: {u'response': {u'steamid': u'76561198040673336', u'success': 1}}
        # example response: {u'response': {u'message': u'No match', u'success': 42}}

        if response['response']['success'] == 1:
            return response['response']['steamid']
        else:
            return False

def getOwnedGames(id):
    API_CALL = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={0}&steamid={1}&format=json&include_played_free_games=1&include_appinfo=1"
    response = requests.get(API_CALL.format(STEAM_API_KEY,id)).json()
    if response['response']['game_count'] > 0:
        return response['response']
    else :
        return False
def getHoursPerGame(library):
    response = {}
    for singlegame in library['games']:
        appid = singlegame['appid']
        response[appid] = singlegame['playtime_forever']
    return response

def getPlayerSummary(id):
    API_CALL = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}"
    response = requests.get(API_CALL.format(STEAM_API_KEY, id)).json()

    if len(response['response']['players']) == 0:
        return False
    else:
        return response['response']['players'][0]

def getPlayerAchievements(id,games):
    API_CALL ="http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid={0}&key={1}&steamid={2}"
    responses = {}
    for game in games['games']:
        responses[game['appid']] = requests.get(API_CALL.format(game['appid'],STEAM_API_KEY, id)).json()
    return responses

def getPlayerAchievementsForSingleGame(id, appid):
    API_CALL = "http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={0}&key={1}&steamid={2}&l=en"
    response = requests.get(API_CALL.format(appid, STEAM_API_KEY, id)).json()
    ps = response['playerstats']

    if "achievements" in ps:
        return sorted(ps['achievements'], key=lambda k: k['achieved'], reverse=True)
    else:
        return dict()
def getTotalAchievements(achievements):
    responses = {}
    for appid in achievements:
        if(len(achievements[appid]) != 0):
            if('achievements' in achievements[appid]['playerstats']):
                responses[appid] = len(achievements[appid]['playerstats']['achievements'])
        else:
            continue
    return responses

def achievementEarned(achievements):
    earnedAchievements = {}
    temp = []
    for appid in achievements:
        if achievements[appid]:
            if 'achievements' in achievements[appid]['playerstats']:
                for i in achievements[appid]['playerstats']['achievements']:
                    temp.append(i['achieved'])
                earnedAchievements[appid] = temp
                temp =[]
    return earnedAchievements

@app.route("/")
def hello():
    vanityUrl = request.args.get("vanityUrl")
    if vanityUrl is None or vanityUrl == "":
        return render_template("index.html")
    else:
        steamId = getSteamIdFromVanityUrl(vanityUrl)
        if steamId == False:
            return render_template("error.html", message="Invalid vanity URL.")
        else:
            data = getOwnedGames(steamId)

            achievements =getPlayerAchievements(steamId, data)
            #for austin
            totalHoursPerGame = getHoursPerGame(data)
            totalPossibleAchievements = getTotalAchievements(achievements)
            earnedAchievement = achievementEarned(achievements)
            numberOfGames = data['game_count']

            data['games'] = sorted(data['games'], key=lambda k: k['playtime_forever'], reverse=True)
            data['playerinfo'] = getPlayerSummary(steamId)
            return render_template("score.html", data=data)

@app.route("/getAchievementsForGame")
def appGetAchievementsForGame():
    steamid = request.args.get("steamid")
    appid = request.args.get("appid")
    if appid is None:
        return "Invalid appid"
    elif steamid is None:
        return "Invalid steamid"

    return render_template("getachievements.html", data=getPlayerAchievementsForSingleGame(steamid, appid))

@app.template_filter('mintohours')
def _jinja2_filter_mintohours(minutes):
    return (minutes / 60)

@app.route("/git-hook", methods=['GET', 'POST'])
def githook():
    return os.popen("git pull; killall python2.7").read()

if __name__ == "__main__":
    app.run()
