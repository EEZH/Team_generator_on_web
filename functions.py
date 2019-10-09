import sqlite3
from classes import Player
import random
import tkinter as tk
import datetime


# определяем текущий год
def cur_year():
    year = datetime.datetime.today()
    year = year.strftime("%Y")
    return year


# получаем список всех игроков из БД
def db_list_getter():
    conn = sqlite3.connect("players_db.db")
    cursor = conn.cursor()

    query_fetch_all = '''
        SELECT * FROM players
    '''

    cursor.execute(query_fetch_all)
    ish_tuple = list(cursor.fetchall())
    conn.commit()
    ish_spisok = []
    for i in ish_tuple:
        ish_spisok.append(list(i))
    return ish_spisok


# получение строки из БД по результатам чек-батона
def ap_list_getter():
    active_players = []
    conn = sqlite3.connect("players_db.db")
    cursor = conn.cursor()
    query_active_players = """
    SELECT * FROM players
    WHERE name = 'self.players[1]'
        """
    cursor.execute(query_active_players)
    conn.commit()
    active_players.append(cursor.fetchall())
    print(active_players)
    return active_players


#  генерация списка экземпляров класса Player из списка активных списков игроков
def players_create(active_players_list):
    players_cl_list = []

    for i in range(len(active_players_list)):
        player = Player(active_players_list[i][1],
                        active_players_list[i][2],
                        active_players_list[i][3],
                        active_players_list[i][4],
                        active_players_list[i][5],
                        active_players_list[i][6],
                        active_players_list[i][7],
                        active_players_list[i][8],
                        active_players_list[i][9])
        players_cl_list.append(player)
    return players_cl_list


# просто вывод атрибутов экзеипляров класса Player
def players_print(players_cl_list):
    for player in players_cl_list:
        print(player.name, player.amplua)


# определяем силы команд
def team_power(team):
    team_power = 0
    for player in team:
        team_power += player.average_stats
        print(player.name)
    print(team_power)
    return team_power


# определяем дельту силы команд
def delta_power(team1, team2):
    delta_team_power = team_power(team1) - team_power(team2)
    return delta_team_power


# калибровка команд
def team_clbr(team_1, team_2):
    clb_index = 1  # индекс чувствительности
    cnt = 0
    while abs(delta_power(team_1, team_2)) > clb_index:
        index_2 = random.randint(0, (len(team_2) - 1))
        index_1 = random.randint(0, (len(team_1) - 1))

        team_1.append(team_2[index_2])  # передали игрока из середины списка сильной команды в слабую
        team_2.remove(team_2[index_2])  # удалили игрока, которого передали в слабую команду

        team_2.append(team_1[index_1])  # передали игрока 2-го по слабости в команду Голых
        team_1.remove(team_1[index_1])  # удалили игрока из команды Зеленых

        cnt += 1
        delta_power(team_1, team_2)

    return team_1, team_2

# отрисовываем окно добавления игрока
def add_user_render():
    top_window = tk.Toplevel()
    top_window.geometry("300x300")
    top_window.title = "Add user"

    lbl_main = tk.Label(top_window, text="Введите информацию:")
    lbl_main.grid(sticky="W", row=0, column=0, columnspan=3)

    input_name = tk.Entry(top_window)
    input_name.grid(sticky="W", row=1, column=1)
    lbl_name = tk.Label(top_window, text="Фамилия и имя:")
    lbl_name.grid(sticky="W", row=1, column=0)

    input_speed = tk.Entry(top_window)
    input_speed.grid(sticky="W", row=2, column=1)
    lbl_speed = tk.Label(top_window, text="Скорость:")
    lbl_speed.grid(sticky="W", row=2, column=0)

    input_stamina = tk.Entry(top_window)
    input_stamina.grid(sticky="W", row=3, column=1)
    lbl_stamina = tk.Label(top_window, text="Выносливость:")
    lbl_stamina.grid(sticky="W", row=3, column=0)

    input_passing = tk.Entry(top_window)
    input_passing.grid(sticky="W", row=4, column=1)
    lbl_passing = tk.Label(top_window, text="Пас:")
    lbl_passing.grid(sticky="W", row=4, column=0)

    input_shot = tk.Entry(top_window)
    input_shot.grid(sticky="W", row=5, column=1)
    lbl_shot = tk.Label(top_window, text="Удар:")
    lbl_shot.grid(sticky="W", row=5, column=0)

    input_teamplay = tk.Entry(top_window)
    input_teamplay.grid(sticky="W", row=6, column=1)
    lbl_teamplay = tk.Label(top_window, text="Командность:")
    lbl_teamplay.grid(sticky="W", row=6, column=0)

    input_goalkeeping = tk.Entry(top_window)
    input_goalkeeping.grid(sticky="W", row=7, column=1)
    lbl_goalkeeping = tk.Label(top_window, text="Навыки вратаря")
    lbl_goalkeeping.grid(sticky="W", row=7, column=0)

    input_amplua = tk.Entry(top_window)
    input_amplua.grid(sticky="W", row=8, column=1)
    lbl_amplua = tk.Label(top_window, text="Амплуа")
    lbl_amplua.grid(sticky="W", row=8, column=0)

    btn_accept_user = tk.Button(top_window, text="Accept")
        #                         , command=lambda: self.on_click(
        # input_name, input_surname, input_age, input_email, input_mobile, root=top_window))
    btn_accept_user.grid(row=10, column=1)
    return top_window


def add_user(self, name, surname, age, email, mobile):
    conn = sqlite3.connect("players_db.db")
    cursor = conn.cursor()
    self.cursor.execute(
        f"""
        INSERT INTO players
        (name, surname, age, email, mobile)
        VALUES(
        "{name}"
        , "{surname}"
        , {age}
        , "{email}"
        , {mobile})
    """)