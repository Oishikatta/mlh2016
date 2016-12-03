import os

from flask import Flask
from flask import render_template

app = Flask(__name__)

STEAM_API_KEY = ""
with open("steam_apikey.txt", mode='r') as apifile:
    STEAM_API_KEY = apifile.read().replace('\n', '')

if len(STEAM_API_KEY) != 32:
    print "Invalid Steam API key. Create steam_apikey.txt before running the app."
    exit()

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/git-hook", methods=['GET', 'POST'])
def githook():
    return os.popen("git pull; killall python2.7").read()

if __name__ == "__main__":
    app.run()
