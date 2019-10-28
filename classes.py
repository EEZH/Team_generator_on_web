# -*- coding: utf-8 -*-
import sqlite3
import hashlib


class Player:
    def __init__(self, id, name, speed, stamina, passing, shot,
                 teamplay, goalkeeping, amplua, average_stats):
        self.id = id
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


class User_control:
    def __init__(self, db_name=None):
        self.conn = sqlite3.connect(db_name, check_same_thread=False) if db_name else None
        self.cursor = self.conn.cursor()

    def get_hash(self, password):
        hash = hashlib.sha1(password.encode())
        result = hash.hexdigest()
        return result

    def authorization(self, user_form):
        query_get_login = """
        SELECT id FROM players
        WHERE login = (?)
        """

        query_get_password = """
        SELECT id FROM passwords
        WHERE user_id = (?) AND password_hash == (?)
        """

        result = self.cursor.execute(query_get_login, (user_form['login'],))

        response = result.fetchone()

        if response is not None:
            result = result.execute(query_get_password, (
                response[0],
                self.get_hash(user_form["pass"])
            ))

            if result.fetchone() is not None:
                return {"status": "ok"}

            return {"status": "err"}
        return {"status": "err"}