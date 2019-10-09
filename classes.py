# -*- coding: utf-8 -*-
class Player:
    def __init__(self, name, speed, stamina, passing, shot,
                 teamplay, goalkeeping, amplua, average_stats):
        self.name = name
        self.speed = float(speed)
        self.stamina = float(stamina)
        self.passing = float(passing)
        self.shot = float(shot)
        self.teamplay = float(teamplay)
        self.goalkeeping = goalkeeping
        self.amplua = amplua
        self.average_stats = float(average_stats)


class List_players:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        return self.players

    def remove_player(self, player):
        self.players.remove(player)
        return self.players
