from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


def web_app_qrscan():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="Сканировать QR",
                                               web_app=WebAppInfo(url="https://192.168.0.1:5173/"))]])
    return kb