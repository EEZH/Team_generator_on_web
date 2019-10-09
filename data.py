from functions import db_list_getter, players_create, cur_year


def players_class_list():
    players = players_create(db_list_getter())
    return players


players = players_class_list()
year = cur_year()
list = []
for player in players:
    list.append(player)
print(list)

