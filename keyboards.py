from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup


def web_app_qrscan():
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Сканировать QR",
                                  web_app=WebAppInfo(url="https://scanner-server.strattonit.ru/"))]])
    return kb