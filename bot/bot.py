import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from bot.settings import (BOT_TOKEN, HEROKU_APP_NAME,
                          WEBHOOK_URL, WEBHOOK_PATH,
                          WEBAPP_HOST, WEBAPP_PORT)
import keyboards as kb
from datetime import datetime
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

import psycopg2
conn = psycopg2.connect(dbname='dd93h7g3uedrn1', user='soxrigiqvchsmn', password='535a584a9a46fa70752593b7f9ec8a7927c6f377515fbb2f87f0fc52c1bb3fb7', host='ec2-23-20-124-77.compute-1.amazonaws.com')
cur = conn.cursor()

cur.execute("SELECT email FROM salesforce.contact;")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

newExpense = [{0: 'id', 1: 'data', 2:'summa', 3: 'description'}]
loginConract = [{0:'login', 1:'pass'}]
botlog = []
balance = '55$'

@dp.message_handler(commands="start")
async def echoStart(message: types.Message):
    if len(botlog) == 0:
        botlog.append(1)
        await message.answer("Введите логин:")
    elif len(botlog) > 0:
        botlog[0] = 1
        await message.answer("Введите логин:")
@dp.message_handler()
async def echoLogin(message: types.Message):
    if botlog[0] == 1:
        await message.answer("Введите пароль:")
        botlog[0] = 2
    elif botlog[0] == 2:
        await message.answer("Авторизация прошла успешно!", reply_markup=kb.inline_kb1)
        await message.answer("Логин или пароль неверны!")
        botlog[0] = 3
    elif botlog[0] == 4:
        try:
            datetime.strptime(message.text, "%Y/%m/%d")
            await message.answer('Введите сумму затрат: ' + message.text)
            botlog[0] = 5
        except ValueError:
            await message.answer('Неправильный ввод даты. Введите дату в формате 2000/05/24')
    elif botlog[0] == 5:
        try:
            int(message.text)
            await message.answer("Введите описание затрат!")
            botlog[0] = 6
        except ValueError:
            await message.answer("Неправильный ввод. Введите сумму!")
    elif botlog[0] == 6:
        await message.answer("Карточка создана!")
        botlog[0] = 0
        await message.answer("Ошибка при создании карты!")
        botlog[0] = 0

@dp.callback_query_handler(lambda c: c.data == 'button1')
async def process_callback_button1(callback_query: types.CallbackQuery):
    if botlog[0] == 3:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Ваш баланс составляет: ' + balance)

@dp.callback_query_handler(lambda c: c.data == 'button2')
async def process_callback_button1(callback_query: types.CallbackQuery):
    if botlog[0] == 3:
        botlog[0] = 4
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'На какой день желаете создать карточку', reply_markup=kb.inline_kb2)
       

@dp.callback_query_handler(lambda c: c.data == 'button3')
async def process_callback_button1(callback_query: types.CallbackQuery):
    if botlog[0] == 4:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Введите сумму затрат: ' + datetime.now().strftime("%Y/%m/%d"))
        botlog[0] = 5


@dp.callback_query_handler(lambda c: c.data == 'button4')
async def process_callback_button1(callback_query: types.CallbackQuery):
    if botlog[0] == 4:
        calendar, step = DetailedTelegramCalendar().build()
        await bot.send_message(callback_query.from_user.id, f"Select {LSTEP[step]}", reply_markup=calendar)
        await bot.answer_callback_query(callback_query.id)
        botlog[0] = 5
        #переменная с выбранной датой

@dp.callback_query_handler(lambda c: c.data == 'button5')
async def process_callback_button1(callback_query: types.CallbackQuery):
    if botlog[0] == 4:
        await bot.answer_callback_query(callback_query.id)
        botlog[0] = 3
        await bot.send_message(callback_query.from_user.id, 'Операция отменена выберете действие',  reply_markup=kb.inline_kb1) 

@dp.callback_query_handler(DetailedTelegramCalendar.func())
async def cal(callback_query: types.CallbackQuery):
    result, key, step = DetailedTelegramCalendar().process(callback_query.data)
    if not result and key:
        await bot.edit_message_text(f"Select {LSTEP[step]}",
                              callback_query.from_user.id,
                              callback_query.message.message_id,
                              reply_markup=key)
    elif result:
        await bot.edit_message_text('Введите сумму затрат:' + f"{result}",
                              callback_query.from_user.id,
                              callback_query.message.message_id)


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
