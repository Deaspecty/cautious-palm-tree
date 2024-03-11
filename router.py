import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
import db_repo
import methods

router = Router()


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
    await m.bot.download(m.photo[-1].file_id, "D:\\PROJECTS\\cheque_scanner\\images\\" + m.photo[-1].file_id + ".jpg")
    logging.info(methods.image_to_text("images\\" + m.photo[-1].file_id + ".jpg"))

