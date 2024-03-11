import asyncio
import logging
from config import *
import coloredlogs as coloredlogs
from aiogram import Bot, Dispatcher
import router


async def start_bot():
    logging.basicConfig(level=logging.DEBUG)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router.router)
    coloredlogs.install()

    asyncio.run(start_bot())

