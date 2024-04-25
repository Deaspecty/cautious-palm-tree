import asyncio
import json
import logging

from aiogram import Dispatcher, Bot
from aiogram.types import Message, WebAppData, ContentType
from db_repo import *
from keyboards import web_app_qrscan
from methods import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
coloredlogs.install(level="INFO")


@dp.message_handler(commands=["start"])
async def start(m: Message):
    if insert_user([str(m.from_user.id), str(m.from_user.username)]):
        kb = web_app_qrscan()
        await m.answer(text=f"Приветствую @{m.from_user.username} 👋"
                            f"\nЯ бот сканер чеков."
                            f"\nОтправьте фотографию чека и я его считаю. 🖼",
                       reply_markup=kb)
    else:
        logging.error("Problems on start")


# @dp.message_handler(content_types=[ContentType.PHOTO])
# async def image(m: Message):
#     file_id = m.photo[-1].file_id
#     image_src = "images\\" + file_id + ".jpg"
#
#     await m.bot.download(file_id, "D:\\PROJECTS\\cheque_scanner\\" + image_src)
#     qr = get_qr_data(image_src)
#     if qr.__len__() != 0:
#         qr_url = qr[0].data
#     else:
#         qr_url = None
#
#     if qr_url is not None:
#         if not_duplicate(user_id=m.from_user.id, qr_url=qr_url):
#             data = format_data(parse_cheque_site(qr_url))
#             if data.__len__() != 0:
#                 json_data = json.dumps(data)
#                 logging.info(f"Чек {image_src} считан: " + str(qr_url))
#                 insert_cheque([str(m.from_user.id), json_data, qr_url, True])
#                 await m.answer(text="Чек считан ✅")
#             else:
#                 insert_cheque([str(m.from_user.id), "", qr_url, False])
#                 await m.bot.send_message(admin_id, text=f"Этот чек не распознан ❗️ "
#                                                         f"\nQR-url: {qr_url}"
#                                                         f"\nUser-id: {m.from_user.id}"
#                                                         f"\nUsername: {m.from_user.username}")
#                 await m.answer(text="Этот тип чеков еще не распознаём, но скоро будем 😄")
#         else:
#             await m.answer(text="Такой чек уже есть в базе данных ❗️")
#     else:
#         await m.answer(text="Чек не распознан ❌")


@dp.message_handler(commands=["mycheques"])
async def get_my_cheques(m: Message):
    user_cheques = get_all_cheques(m.from_user.id, verified=True)
    print(user_cheques)
    if len(user_cheques) != 0:
        text = beautifulize_data_all(user_cheques)
        await m.answer(text=text)
    else:
        await m.answer(text="У вас еще нет чеков 📝")


# @dp.message_handler(content_types=[ContentType.DOCUMENT])
# async def image(m: Message):
#     if m.document.mime_type == "image/png":
#         file_id = m.document.file_id
#         image_src = "images\\" + file_id + ".jpg"
#
#         await m.bot.download(file_id, "D:\\PROJECTS\\cheque_scanner\\" + image_src)
#         qr = get_qr_data(image_src)
#         if qr.__len__() != 0:
#             qr_url = qr[0].data
#         else:
#             qr_url = None
#
#         if qr_url is not None:
#             if not_duplicate(user_id=m.from_user.id, qr_url=qr_url):
#                 data = format_data(parse_cheque_site(qr_url))
#                 if data.__len__() != 0:
#                     json_data = json.dumps(data)
#                     logging.info(f"Чек {image_src} считан: " + str(qr_url))
#                     insert_cheque([str(m.from_user.id), json_data, qr_url, True])
#                     await m.answer(text="Чек считан ✅")
#                 else:
#                     insert_cheque([str(m.from_user.id), "", qr_url, False])
#                     await m.bot.send_message(admin_id, text=f"Этот чек не распознан ❗️ "
#                                                             f"\nQR-url: {qr_url}"
#                                                             f"\nUser-id: {m.from_user.id}"
#                                                             f"\nUsername: {m.from_user.username}")
#                     await m.answer(text="Этот тип чеков еще не распознаём, но скоро будем 😄")
#             else:
#                 await m.answer(text="Такой чек уже есть в базе данных ❗️")
#         else:
#             await m.answer(text="Чек не распознан ❌")


@dp.message_handler(content_types="web_app_data")
async def asd(message: Message):
    DEV_MODE = False
    if DEV_MODE:
        url = "http://consumer.oofd.kz?i=1858674569&f=010100658756&s=3800.00&t=20240410T144420"
    else:
        url = message.web_app_data.data
    msg = await message.answer(text="Обрабатываю чек...")
    data = format_data(parse_cheque_site(url))
    if data.__len__() != 0:
        insert_cheque(user_id=message.from_user.id, qr_url=url, verified=True, cheque_json=json.dumps(data))
        for row in data["no_format_header"].split("\n"):
            data.update(search_in_text(row))
        print(data)
        text = beautifulize_data_one(data)
        print(text)
        await msg.edit_text(text=text)
    else:
        insert_cheque(user_id=message.from_user.id, qr_url=url, verified=False)
        await msg.edit_text(text="Не удалось обработать чек")


@dp.message_handler(commands=["test"])
async def asd(message: Message):
    url = "http://consumer.oofd.kz?i=2673764153&f=010102274600&s=1890.00&t=20231210T151300"
    msg = await message.answer(text="Обрабатываю чек...")
    data = format_data(parse_cheque_site(url))
    if data.__len__() != 0:
        insert_cheque(user_id=message.from_user.id, qr_url=url, verified=True, cheque_json=json.dumps(data))
        for row in data["no_format_header"].split("\n"):
            print(90)
            data.update(search_in_text(row))
        text = beautifulize_data_one(data)
        print(text)
        await msg.edit_text(text=text)
    else:
        insert_cheque(user_id=message.from_user.id, qr_url=url, verified=False)
        await msg.edit_text(text="Не удалось обработать чек")


async def start_bot():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
