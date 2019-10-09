from flask import Flask, render_template, request, redirect
from data import players_class_list, players, year, list

from functions import db_list_getter
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", year=year)


@app.route("/team_gen/", methods=["GET", "POST"])
def team_gen():
    active_players = []
    a = dict(
        active=request.form["list[player.name]"]
    )
    active_players.append(a)

    print(active_players)
    return render_template("team_gen.html", players=players, year=year)


@app.route("/players/")
def players_list():
    return render_template("players_list.html", players=players, year=year)


if __name__ == "__main__":
    app.run(debug=True)