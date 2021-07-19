import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT)
import psycopg2
import psycopg2.extras

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

conn = psycopg2.connect(dbname='dd93h7g3uedrn1', user='soxrigiqvchsmn', password='535a584a9a46fa70752593b7f9ec8a7927c6f377515fbb2f87f0fc52c1bb3fb7', host='ec2-23-20-124-77.compute-1.amazonaws.com')

botlog = []

@dp.message_handler(commands="start")
async def echoStart(message: types.Message):
    if len(botlog) == 0:
        botlog.append(1)
        await message.answer("Введите логин:")
    elif len(botlog) > 0:
        botlog[0] = 1
        await message.answer("Введите логин:")



async def on_startup(dp):
    logging.warning(
        'Starting connection. ')
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)


async def on_shutdown(dp):
    logging.warning('Bye! Shutting down webhook connection')


def main():
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

conn.close()