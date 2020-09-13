from artistry import app
from flask import render_template, redirect, request
from artistry.core.graph import getGraph
from artistry.core.genius import find_connection


@app.route("/")
def index():
    return redirect("/search_artist/")


@app.route("/search_artist/", methods=["GET", "POST"])
def searchArtist():
    if request.method == "POST":
        artistName = request.form["artistName"]
        connections = find_connection(artistName)
        img = getGraph(artistName, connections)
        return render_template("artist_info.html", img=img)

    return render_template("search_artist.html")
