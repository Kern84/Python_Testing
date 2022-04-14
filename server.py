import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    with open("clubs.json") as c:
        listOfClubs = json.load(c)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("competitions.json") as comps:
        listOfCompetitions = json.load(comps)["competitions"]
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()

place_points = 3


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    input_email = request.form["email"]
    list_club_email = []
    for element in clubs:
        list_club_email.append(element["email"])
    if input_email in list_club_email:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
        return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash("Sorry, that email wasn't found, please try again.")
        return render_template("index.html")


@app.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
    except IndexError:
        foundClub = None

    try:
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
    except IndexError:
        foundCompetition = None

    if foundClub and foundCompetition:
        if foundCompetition["date"] > str(datetime.now()):
            if int(foundCompetition["numberOfPlaces"]) > 0:
                flash("Valid competition")
                return render_template(
                    "booking.html", club=foundClub, competition=foundCompetition
                )
            else:
                flash("Something went wrong-please try again")
                return render_template(
                    "welcome.html", club=foundClub, competitions=competitions
                )
        else:
            flash("You cannot book places for a past competition")
            return render_template(
                "welcome.html", club=foundClub, competitions=competitions
            )
    elif foundClub:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html", club=foundClub, competitions=competitions
        )
    else:
        flash("Something went wrong-please try again")
        return redirect(url_for("index"))


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])

    if placesRequired > 0 and placesRequired <= 12:
        if int(club["points"]) >= (placesRequired * place_points):
            competition["numberOfPlaces"] = (
                int(competition["numberOfPlaces"]) - placesRequired
            )
            club["points"] = int(club["points"]) - (placesRequired * place_points)
            flash("Great-booking complete!")
            return render_template("welcome.html", club=club, competitions=competitions)
        else:
            flash("You do not have enough points to make this booking")
            return render_template("welcome.html", club=club, competitions=competitions)
    else:
        flash("You must register a positive number of places (between 1 and 12)")
        return render_template("booking.html", club=club, competition=competition)


@app.route("/displayPoints")
def displayPoints():
    return render_template("display.html", clubs=clubs)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
