import logging
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