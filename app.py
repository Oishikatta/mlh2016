from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/git-hook", methods=['GET', 'POST'])
def githook():
    return os.popen("git pull").read()

if __name__ == "__main__":
    app.run()
