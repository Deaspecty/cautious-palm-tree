import json
import logging

import coloredlogs
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import db_repo
import methods

router = Router()
coloredlogs.install(level="INFO")


@router.message(Command("start"))
async def start(m: Message):
    if db_repo.insert_user([str(m.from_user.id), str(m.from_user.username)]):
        await m.answer(text=f"Приветствую @{m.from_user.username} 👋"
                            f"\nЯ бот сканер чеков."
                            f"\nОтправьте фотографию чека и я его считаю. 🖼")
    else:
        logging.error("Problems on start")


@router.message(F.photo)
async def image(m: Message):
    file_id = m.photo[-1].file_id
    image_src = "images\\" + file_id + ".jpg"

    await m.bot.download(file_id, "D:\\PROJECTS\\cheque_scanner\\" + image_src)
    image_text = methods.image_to_text(image_src)
    qr_data = methods.get_qr_data(image_src)[0].data

    if qr_data is not None:
        json_data = json.dumps({"imageText": image_text})  # todo заменить на парсер с ссылкой на сайт с чеком
        logging.info(f"Чек {image_src} считан: " + str(qr_data))
        db_repo.insert_cheque([str(m.from_user.id), json_data, qr_data])
        await m.answer(text="Чек считан: " + str(qr_data))
    else:
        await m.answer(text="Чек не распознан")