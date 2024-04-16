import asyncio
import logging
from aiogram.utils.web_app import check_webapp_signature
import config
from config import *
import coloredlogs as coloredlogs
from aiogram import Bot, Dispatcher, F
import router


async def start_bot():
    logging.basicConfig(level=logging.DEBUG)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
dp.include_routers(router.router)
coloredlogs.install(level="DEBUG")


if __name__ == '__main__':
    asyncio.run(start_bot())
    # отправляем сообщение в ответ на отправку данных из веб-приложения
