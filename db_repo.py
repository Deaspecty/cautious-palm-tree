from config import *


def insert(columns, values, table, filter):
    if len(columns) == len(values) and len(columns) != 0:
        columns = ", ".join(columns)
        values = ", ".join(values)
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO cheque_bot.users_data({columns}) VALUES ({values})")