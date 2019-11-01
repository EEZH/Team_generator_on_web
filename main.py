from flask import Flask, render_template, request, session, redirect
from functions import team_power, delta_power, team_clbr, players, year, players_photo_list, \
    all_players_create, db_list_getter
import json
from classes import User_control
from constants import MENU_WITH_SESSION, MENU_WITHOUT_SESSION, MENU_WITH_SESSION_ADMIN

application = Flask(__name__)
userControl = User_control("players_db.db")

with open("config.json", "r") as f:
    o = json.load(f)
    application.secret_key = o['secret_key']


@application.route("/", methods=["GET", "POST"])
def authorization():
    if request.method == "GET":
        if session.get('player') == "ZhurEvg":
            return render_template("home.html", user_name=session["player"], menu_items=MENU_WITH_SESSION_ADMIN,
                                   year=year)
        if session.get("player"):
            return render_template("home.html", user_name=session["player"], menu_items=MENU_WITH_SESSION, year=year)
        return render_template("form_authorization.html", menu_items=MENU_WITHOUT_SESSION, year=year)

    result = userControl.authorization(request.form)
    if result["status"] == "ok":
        session["player"] = request.form["login"]
        return redirect("/")

    return render_template("form_authorization.html", menu_items=MENU_WITHOUT_SESSION, is_err=True, year=year)


@application.route("/logout/")
def logout():
    session.pop("player")
    return redirect("/")


@application.route("/home/")
def home():
    return render_template("home.html", year=year)


@application.route("/team_gen/", methods=["GET", "POST"])
def team_gen():
    photos = players_photo_list(all_players_create(db_list_getter()))
    players_with_photos = photos[0]
    players_without_photos = photos[1]
    if request.method == "GET":
        if session.get('player') == "ZhurEvg":
            return render_template("team_gen.html", players=players_with_photos, sec_players=players_without_photos,
                                   year=year, menu_items=MENU_WITH_SESSION_ADMIN)
        if session.get("player"):
            return render_template("team_gen.html", players=players_with_photos, sec_players=players_without_photos,
                                   year=year, menu_items=MENU_WITH_SESSION)

    active_players = request.form.getlist("myPlayer")
    if len(active_players) >= 2:

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
            if len(active_payers_list()) < 2:
                print("Выбрано мало игроков")
            else:
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

        delta_power_loc = delta_power(team_creator()[0], team_creator()[1])
        clbr = team_clbr(team_creator()[0], team_creator()[1])
        team1 = clbr[0]
        team2 = clbr[1]
        if session.get('player') == "ZhurEvg":
            return render_template("teams.html", players=players, year=year, team1=team1, team1_power=team_power(team1),
                                   team2=team2, team2_power=team_power(team2), menu_items=MENU_WITH_SESSION_ADMIN)
        if session.get('player'):
            return render_template("teams.html", players=players, year=year, team1=team1, team1_power=team_power(team1),
                                   team2=team2, team2_power=team_power(team2), menu_items=MENU_WITH_SESSION)
    else:
        if session.get('player') == "ZhurEvg":
            return render_template("team_gen.html", players=players_with_photos, sec_players=players_without_photos,
                                   year=year, menu_items=MENU_WITH_SESSION_ADMIN)
        if session.get('player'):
            return render_template("team_gen.html", players=players_with_photos, sec_players=players_without_photos,
                                   year=year, menu_items=MENU_WITH_SESSION)


@application.route("/teams/")
def teams():
    if session.get('player') == "ZhurEvg":
        return render_template("teams.html", year=year, menu_items=MENU_WITH_SESSION_ADMIN, players=players)
    if session.get('player'):
        return render_template("teams.html", year=year, menu_items=MENU_WITH_SESSION, players=players)


@application.errorhandler(UnboundLocalError)
def zero_player(error):
    if session.get('player') == "ZhurEvg":
        return render_template("zero_player.html", menu_items=MENU_WITH_SESSION_ADMIN)
    if session.get('player'):
        return render_template("zero_player.html", menu_items=MENU_WITH_SESSION)


@application.errorhandler(404)
def not_found(error):
    if session.get('player') == "ZhurEvg":
        return render_template("404.html", page="not found", menu_items=MENU_WITH_SESSION_ADMIN)
    if session.get('player'):
        return render_template("404.html", page="not found", menu_items=MENU_WITH_SESSION)


@application.route("/players/")
def players_list():
    photos = players_photo_list(all_players_create(db_list_getter()))
    players_with_photos = photos[0]
    players_without_photos = photos[1]
    if session.get('player') == "ZhurEvg":
        return render_template("players_list.html", players=players_with_photos, sec_players=players_without_photos,
                               year=year, menu_items=MENU_WITH_SESSION_ADMIN)
    if session.get('player'):
        return render_template("players_list.html", players=players_with_photos, sec_players=players_without_photos,
                               year=year, menu_items=MENU_WITH_SESSION)


@application.route("/add_player/", methods=["GET", "POST"])
def user_control():
    if session.get('player') == "ZhurEvg":
        if request.method == "POST":
            new_player = request.form
            new_player_amplua = request.form["amplua"]
            print(new_player)
            print(new_player_amplua)
            userControl.add_player(new_player)
            # return redirect(f"/users?id={id}")
        return render_template("add_player_form.html", page="add user", year=year, menu_items=MENU_WITH_SESSION_ADMIN,
                               players=players)


@application.route("/user_form/", methods=["GET", "POST"])
def user_config():
    if request.method == "GET":
        if session.get('player') == "ZhurEvg":
            return render_template("user_form.html", user_name=session["player"], menu_items=MENU_WITH_SESSION_ADMIN,
                                   year=year, us_value=session.get('player'))
        if session.get("player"):
            return render_template("user_form.html", user_name=session["player"], menu_items=MENU_WITH_SESSION, year=year)
        return render_template("form_authorization.html", menu_items=MENU_WITHOUT_SESSION, year=year)
    if request.method == "POST":
        new_params = request.form
        result = userControl.user_config(request.form)
        # print(new_params)
        return render_template("form_authorization.html", menu_items=MENU_WITHOUT_SESSION, is_err=True, year=year)
    return render_template("form_authorization.html", menu_items=MENU_WITHOUT_SESSION, is_err=True, year=year)


if __name__ == "__main__":
    application.run(debug=True)
