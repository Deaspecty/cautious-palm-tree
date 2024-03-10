import logging
from config import *
import coloredlogs as coloredlogs
import pytesseract
import cv2
from aiogram import Bot, Dispatcher
import router


def image_to_text(filename):
    image = cv2.imread(filename)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    return pytesseract.image_to_string(image, lang="rus+eng", config=r'--oem 3')


async def start_bot():
    logging.basicConfig(level=logging.DEBUG)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_routers(router.router, callback_router.router)
    coloredlogs.install()

    asyncio.run(start_bot())
    # печатаем
    print(image_to_text("check-subtotal-1.jpg"))
