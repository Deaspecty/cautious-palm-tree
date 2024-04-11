import json
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from db_repo import *
from keyboards import web_app_qrscan
from methods import *

router = Router()
coloredlogs.install(level="DEBUG")


@router.message(Command("start"))
async def start(m: Message):
    if insert_user([str(m.from_user.id), str(m.from_user.username)]):
        kb = web_app_qrscan()
        await m.answer(text=f"Приветствую @{m.from_user.username} 👋"
                            f"\nЯ бот сканер чеков."
                            f"\nОтправьте фотографию чека и я его считаю. 🖼",
                       reply_markup=kb)
    else:
        logging.error("Problems on start")


@router.message(F.photo)
async def image(m: Message):
    file_id = m.photo[-1].file_id
    image_src = "images\\" + file_id + ".jpg"

    await m.bot.download(file_id, "D:\\PROJECTS\\cheque_scanner\\" + image_src)
    qr = get_qr_data(image_src)
    if qr.__len__() != 0:
        qr_url = qr[0].data
    else:
        qr_url = None

    if qr_url is not None:
        if not_duplicate(user_id=m.from_user.id, qr_url=qr_url):
            data = format_data(parse_cheque_site(qr_url))
            if data.__len__() != 0:
                json_data = json.dumps(data)
                logging.info(f"Чек {image_src} считан: " + str(qr_url))
                insert_cheque([str(m.from_user.id), json_data, qr_url, True])
                await m.answer(text="Чек считан ✅")
            else:
                insert_cheque([str(m.from_user.id), "", qr_url, False])
                await m.bot.send_message(admin_id, text=f"Этот чек не распознан ❗️ "
                                                        f"\nQR-url: {qr_url}"
                                                        f"\nUser-id: {m.from_user.id}"
                                                        f"\nUsername: {m.from_user.username}")
                await m.answer(text="Этот тип чеков еще не распознаём, но скоро будем 😄")
        else:
            await m.answer(text="Такой чек уже есть в базе данных ❗️")
    else:
        await m.answer(text="Чек не распознан ❌")


@router.message(Command("mycheques"))
async def get_my_cheques(m: Message):
    user_cheques = get_all_cheques(m.from_user.id)
    cheques_str = ""
    if len(user_cheques) != 0:
        for row in range(len(user_cheques)):
            cheques_str += f"{row + 1}) {user_cheques[row][3]}\n"
        await m.answer(text=cheques_str)
    else:
        await m.answer(text="У вас еще нет чеков 📝")


@router.message(F.document)
async def image(m: Message):
    if m.document.mime_type == "image/png":
        file_id = m.document.file_id
        image_src = "images\\" + file_id + ".jpg"

        await m.bot.download(file_id, "D:\\PROJECTS\\cheque_scanner\\" + image_src)
        qr = get_qr_data(image_src)
        if qr.__len__() != 0:
            qr_url = qr[0].data
        else:
            qr_url = None

        if qr_url is not None:
            if not_duplicate(user_id=m.from_user.id, qr_url=qr_url):
                data = format_data(parse_cheque_site(qr_url))
                if data.__len__() != 0:
                    json_data = json.dumps(data)
                    logging.info(f"Чек {image_src} считан: " + str(qr_url))
                    insert_cheque([str(m.from_user.id), json_data, qr_url, True])
                    await m.answer(text="Чек считан ✅")
                else:
                    insert_cheque([str(m.from_user.id), "", qr_url, False])
                    await m.bot.send_message(admin_id, text=f"Этот чек не распознан ❗️ "
                                                            f"\nQR-url: {qr_url}"
                                                            f"\nUser-id: {m.from_user.id}"
                                                            f"\nUsername: {m.from_user.username}")
                    await m.answer(text="Этот тип чеков еще не распознаём, но скоро будем 😄")
            else:
                await m.answer(text="Такой чек уже есть в базе данных ❗️")
        else:
            await m.answer(text="Чек не распознан ❌")



