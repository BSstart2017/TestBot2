import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT)
import os
import psycopg2

DATABASE_URL = os.environ['postgres://soxrigiqvchsmn:535a584a9a46fa70752593b7f9ec8a7927c6f377515fbb2f87f0fc52c1bb3fb7@ec2-23-20-124-77.compute-1.amazonaws.com:5432/dd93h7g3uedrn1']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands="start")
async def echoStart(message: types.Message):
    await message.answer("Введите логин:")
    await message.answer(cur)
    global botlog
    botlog = 'Введите логин:'

@dp.message_handler()
async def echoLogin(message: types.Message):
    if botlog == 'Введите логин:':
        global loginUser
        loginUser = message.text
        await message.answer("Введите пароль:")
        

@dp.message_handler()
async def echoPass(message: types.Message):
    if botlog == 'Введите пароль:':
        global loginPass
        loginPass = message.text
        await message.answer("Пароль:" + loginPass)
        await message.answer("Успех")
        

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

cur.close()
conn.close()
