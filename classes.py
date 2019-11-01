# -*- coding: utf-8 -*-
import sqlite3
import hashlib
from flask import session


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
        self.goalkeeping = float(goalkeeping)
        self.amplua = amplua
        average_stats = (self.speed + self.stamina + self.passing + self.shot + self.teamplay) / 5
        self.average_stats = average_stats


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
        self.cursor = self.conn.cursor() if self.conn else None

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

    def add_player(self, new_player):

        query_to_users = lambda new_player: f"""
        INSERT INTO PLAYERS
               (name, speed, stamina, passing, shot, teamplay, goalkeeping, amplua, average_stats, login)
               VALUES
               ("{new_player["name"]}"
               ,{new_player["speed"]}
               ,{new_player["stamina"]}
               ,{new_player["passing"]}
               ,{new_player["shot"]}
               ,{new_player["teamplay"]}
               ,{new_player["goalkeeping"]}
               ,"{new_player["amplua"]}"
                , (({float(new_player["speed"])}+{float(new_player["passing"])}
                +{float(new_player["stamina"])}+{float(new_player["shot"])}
                +{float(new_player["teamplay"])})/5)
               ,"{new_player["login"]}"
               )
               """
        self.cursor.execute(query_to_users(new_player))

        password = '12345'
        hash = hashlib.sha1(password.encode())
        hash_result = hash.hexdigest()

        query_id = f"""
        SELECT id FROM PLAYERS
        WHERE login = "{new_player["login"]}"
        """
        self.cursor.execute(query_id)
        new_player_id = self.cursor.fetchone()[0]
        print(new_player_id)

        query_to_passwords = lambda hash_result, user_id: f"""
        INSERT INTO passwords
        (password_hash, user_id)
        VALUES
        ("{hash_result}"
        , "{new_player_id}"
        )
        """
        self.cursor.execute(query_to_passwords(hash_result, new_player_id))
        self.conn.commit()

        return new_player_id

    def user_config(self, new_params):
        #получаем ID залогининого юзера
        query_get_login = f"""
                SELECT id FROM PLAYERS
                WHERE login = "{ session.get('player') }"
"""

        result_user_id = self.cursor.execute(query_get_login)
        response_id = result_user_id.fetchone()[0]

        # получаем хэш пароля залогиненного юзера
        query_get_password = f"""
                SELECT password_hash FROM passwords
                WHERE user_id = { response_id }
                """

        result_user_pass = self.cursor.execute(query_get_password)
        response_pass_from_bd = result_user_pass.fetchone()[0]

        cur_pass_from_form = self.get_hash(new_params["cur_pass"])
        print(cur_pass_from_form)

        new_login = new_params["new_login"]

        new_pass_from_form = self.get_hash(new_params["new_pass"])
        new_pass_acc = self.get_hash(new_params["new_pass_acc"])

        print(new_login, new_pass_from_form, new_pass_acc)

        query_to_passwords = lambda new_pass_acc, user_id: f"""
        UPDATE passwords
        SET password_hash = "{new_pass_acc}"
        WHERE user_id = {response_id}
        """

        query_to_users = lambda new_player: f"""
        UPDATE PLAYERS
        SET login = "{new_login}"
        WHERE id = { response_id }
               """

        if response_pass_from_bd == cur_pass_from_form:
            self.cursor.execute(query_to_passwords(new_pass_acc, response_id))
            self.cursor.execute(query_to_users(new_pass_acc))
            self.conn.commit()

        #
        # print(response_id)
        # print(response_pass_from_bd)

        return response_id

        #
        # if response is not None:
        #     result = result.execute(query_get_password, (
        #         response[0],
        #         self.get_hash(user_form["pass"])
        #     ))
        #
        #     if result.fetchone() is not None:
        #         return {"status": "ok"}
        #
        #     return {"status": "err"}
        # return {"status": "err"}
