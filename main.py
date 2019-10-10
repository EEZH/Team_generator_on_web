from flask import Flask, render_template, request, redirect
from data import players_class_list, players, year, a

from functions import db_list_getter

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", year=year)


@app.route("/team_gen/", methods=["GET", "POST"])
def team_gen():
    if request.method == "GET":
        return render_template("team_gen.html", players=players, year=year)
    list = []
    active = dict(
    player=request.form["name"]
    )
    list.append(active)
    print(list)
    return render_template("team_gen.html", players=players, year=year)



@app.route("/players/")
def players_list():
    return render_template("players_list.html", players=players, year=year)


if __name__ == "__main__":
    app.run(debug=True)
