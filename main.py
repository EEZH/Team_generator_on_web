from flask import Flask, render_template, request, redirect
from data import players, year
from functions import team_power, delta_power, team_clbr

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html", year=year)


@app.route("/team_gen/", methods=["GET", "POST"])
def team_gen():
    if request.method == "GET":
        return render_template("team_gen.html", players=players, year=year)

    active_players = request.form.getlist("myPlayer")

    # формируем список экземпляров класса Player из активных игроков
    def active_payers_list():
        active_players_list = []
        for myPlayer in players:
            for act_player in active_players:
                if act_player == myPlayer.name:
                    active_players_list.append(myPlayer)
        return active_players_list

    # определям количество игроков в командах
    def div_players_team(active_players_list):
        team_1_cnt = len(active_payers_list()) // 2
        team_2_cnt = len(active_payers_list()) - team_1_cnt

        return team_1_cnt, team_2_cnt

    # формируем команды
    def team_creator():
        team_1 = []
        team_2 = []

        # формируем команду №1
        for i in range(div_players_team(active_payers_list())[0]):
            team_1.append(active_payers_list()[i])

        # формируем команду №2
        for i in range(div_players_team(active_payers_list())[0],
                       div_players_team(active_payers_list())[0] + div_players_team(active_payers_list())[1]):
            team_2.append(active_payers_list()[i])

        return team_1, team_2

    teams = team_creator()
    print(teams)

    delta_power_loc = delta_power(team_creator()[0], team_creator()[1])
    clbr = team_clbr(team_creator()[0], team_creator()[1])
    team1 = clbr[0]
    team2 = clbr[1]

    return render_template("teams.html", players=players, year=year, team1=team1, team1_power=team_power(team1),
                           team2=team2, team2_power=team_power(team2))


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", page="not found")


@app.route("/teams/")
def teams():
    return render_template("teams.html", year=year)


@app.route("/players/")
def players_list():
    return render_template("players_list.html", players=players, year=year)


if __name__ == "__main__":
    app.run(debug=True)
