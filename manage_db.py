import sqlite3
import hashlib
from functions import all_players_create, db_list_getter


def get_hash(password: str) -> str:
    hash = hashlib.sha1(password.encode())
    result = hash.hexdigest()
    return result


query_create_table_passwords = """
    CREATE TABLE passwords (
    id INTEGER PRIMARY KEY
    , password_hash VARCHAR(200) NOT NULL
    , user_id INTEGER NOT NULL 
    )
"""

conn = sqlite3.connect("players_db.db")

cursor = conn.cursor()


# cursor.execute(query_create_table_passwords)
# conn.rollback()
# cursor.execute("""DROP TABLE users_data""")

# генерим транспортные пароли юзерам
def pass_gen():
    players_passwords = []
    ish_spisok = db_list_getter()
    class_list = all_players_create(ish_spisok)
    for player in class_list:
        players_passwords.append((get_hash("12345"), player.id), )
    return players_passwords


# players_passwords = pass_gen()
# print(players_passwords)

query_add_passwords = """
    INSERT INTO passwords
    (password_hash, user_id)
    VALUES(?, ?) 
"""

# cursor.executemany(query_add_passwords, pass_gen())
# conn.commit()
