import sqlite3
from classes import Player
import random
import datetime
import os


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
    # print(active_players)
    return active_players


#  генерация списка экземпляров класса Player из списка активных игроков
def players_create(active_players_list):
    players_cl_list = []

    for i in range(len(active_players_list)):
        player = Player(active_players_list[i][0],
                        active_players_list[i][1],
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


#  генерация списка экземпляров класса Player из списка всех игроков
def all_players_create(ish_spisok):
    players_class_list = []

    for i in range(len(ish_spisok)):
        player = Player(ish_spisok[i][0],
                        ish_spisok[i][1],
                        ish_spisok[i][2],
                        ish_spisok[i][3],
                        ish_spisok[i][4],
                        ish_spisok[i][5],
                        ish_spisok[i][6],
                        ish_spisok[i][7],
                        ish_spisok[i][8],
                        ish_spisok[i][9])
        players_class_list.append(player)

    return players_class_list


# просто вывод атрибутов экзеипляров класса Player
def players_print(players_cl_list):
    for player in players_cl_list:
        print(player.name, player.amplua)


# определяем силы команд
def team_power(team):
    team_power = 0
    for player in team:
        team_power += player.average_stats
    return round(team_power, 3)


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
        if cnt > 10000:
            gen_error = "Не удается сформировать равные команды из выбранных игроков!"
            print(gen_error)
            break
    return team_1, team_2


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


# перебор файлов в папке
def file_list():
    directory = "static/photos"
    files = os.listdir(directory)
    images = []
    for file in files:
        if file.endswith(".jpg") or file.endswith(".png"):
            images.append(file)
    return images


# создание двух списков игроков: с фото и без
def players_photo_list(players):
    images = file_list()
    player_with_photo = []
    player_without_photo = []
    for player in all_players_create(db_list_getter()):
        for image in images:
            if str(player.id) + ".jpg" == image or str(player.id) + ".png" == image:
                player_with_photo.append(player)
                break
        else:
            player_without_photo.append(player)
    return player_with_photo, player_without_photo


def players_class_list():
    players = all_players_create(db_list_getter())
    # print(players)
    return players


name_list = []
players = players_class_list()
for player in players:
    name_list.append(player.name)
# print((name_list))
year = cur_year()


def list_form():
    list = []
    for player in players:
        PLAYER = [
            dict(name=player.name, average_stats=player.average_stats)
        ]
        list.append(PLAYER)
    return list

