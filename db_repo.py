import coloredlogs
from config import *

coloredlogs.install()


def insert_user(data) -> bool:
    if len(data) != 0:
        query = f"INSERT INTO cheque_bot.users_data(user_id, username) VALUES (%s, %s)"
        cursor = con.cursor()
        cursor.execute(query, data)
        con.commit()
        cursor.close()
        return True
    else:
        return False


def get_user(user_id) -> list:
    query = f"SELECT * FROM cheque_bot.users_data WHERE user_id = '{user_id}'"
    cursor = con.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


def insert_cheque(data) -> bool:
    if len(data) != 0:
        query = f"INSERT INTO cheque_bot.cheques(user_id, cheque_json) VALUES (%s, %s)"
        cursor = con.cursor()
        cursor.execute(query, data)
        con.commit()
        cursor.close()
        return True
    else:
        return False