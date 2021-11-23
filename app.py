from pprint import pprint
from re import purge
from flask import Flask, redirect, url_for, render_template, request
import playlist as pl
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/in', methods=["POST","GET"])
def inputplaylist():
    if request.method == "POST":
        pUrl = request.form["playlistURL"]
        return pl.getPlaylistInformation(pUrl)
    else:
        return render_template("login.html")




if __name__ == "__main__":
    app.run(debug=True)