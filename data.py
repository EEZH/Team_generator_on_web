from functions import db_list_getter, players_create, cur_year


def players_class_list():
    players = players_create(db_list_getter())
    print(players)
    return players

name_list = []
players = players_class_list()
for player in players:
    name_list.append(player.name)
print((name_list))
year = cur_year()

def list_form():
    list = []
    for player in players:
        PLAYER = [
            dict(name=player.name, average_stats=player.average_stats)
        ]
        list.append(PLAYER)
    return list
a = list_form()

#
# USERS = [
#     dict(name="Harry", surname="Potter", age=19),
#     dict(name="Hermiona", surname="Granger", age=21),
#     dict(name="Rohan", surname="Pops", age=23),
#     dict(name="Albus", surname="Dumbledor", age=150),
#     dict(name="Severus", surname="Snag", age=56)
# ]

