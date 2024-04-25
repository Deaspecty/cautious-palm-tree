import logging

import coloredlogs
from config import *

coloredlogs.install(level="DEBUG")


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
        query = f"INSERT INTO cheque_bot.cheques(user_id, cheque_json, qr_url, verified) VALUES (%s, %s, %s, %s)"
        cursor = con.cursor()
        cursor.execute(query, data)
        con.commit()
        cursor.close()
        return True
    else:
        return False


def insert_cheque(user_id, qr_url, verified, cheque_json=None) -> bool:
    logging.info("insert_cheque")
    if verified:
        query = f"INSERT INTO cheque_bot.cheques(user_id, qr_url, verified, cheque_json) VALUES (%s, %s, %s, %s)"
        cursor = con.cursor()
        cursor.execute(query, [str(user_id), qr_url, verified, cheque_json])
        con.commit()
        cursor.close()
        return True
    else:
        query = f"INSERT INTO cheque_bot.cheques(user_id, qr_url, verified) VALUES (%s, %s, %s)"
        cursor = con.cursor()
        cursor.execute(query, [user_id, qr_url, verified])
        con.commit()
        cursor.close()
        logging.info("Инсерт чек")
        return False


def not_duplicate(user_id, qr_url):
    cursor = con.cursor(buffered=True)
    cursor.execute("SELECT user_id, qr_url FROM cheques WHERE user_id=%s and qr_url=%s", (user_id, qr_url))
    user_cheque = cursor.fetchall()
    logging.info(f"user_id: {user_id}; {len(user_cheque)} cheques in db")
    if len(user_cheque) == 0:
        return True
    else:
        return False


def get_all_cheques(user_id, verified=False):
    if verified:
        query = f"SELECT * FROM cheques WHERE user_id=%s and verified=%s"
        cursor = con.cursor()
        cursor.execute(query, (user_id, verified))
    else:
        query = f"SELECT * FROM cheques WHERE user_id=%s"
        cursor = con.cursor()
        cursor.execute(query, (user_id,))
    result = cursor.fetchall()
    cursor.close()
    return result