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
from datetime import datetime
import keyboards as kb

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

@dp.message_handler()
async def echoLogin(message: types.Message):
    if botlog[0] == 1:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as contact:
            contact.execute(("SELECT * FROM salesforce.contact where email='{}';").format(message.text))
            if len(contact.fetchall()) == 1:
                if len(botlog) == 1:
                    botlog.append(1)
                else:
                    botlog[1] = 1
            else:
                if len(botlog) == 1:
                    botlog.append(0)
                else:
                    botlog[1] = 0
        await message.answer("Введите пароль:")
        botlog[0] = 2
    elif botlog[0] == 2:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as contact:
            contact.execute(("SELECT * FROM salesforce.contact where password__c='{}';").format(message.text))
            if len(contact.fetchall()) == 1:
                if len(botlog) == 2:
                    botlog.append(1)
                else:
                    botlog[2] = 1
            else:
                if len(botlog) == 2:
                    botlog.append(0)
                else:
                    botlog[2] = 0
            if botlog[1] == 1 & botlog[2] == 1:
                await message.answer("Авторизация прошла успешно!", reply_markup=kb.inline_kb1)
                botlog[0] = 3
                global userId
                contact.execute(("SELECT * FROM salesforce.contact where password__c='{}';").format(message.text))
                userId = str(contact.fetchone()['sfid'])
            else:
                await message.answer("Логин или пароль неверны!")
                botlog[0] = 0
    elif botlog[0] == 4:
        try:
            if datetime.strptime(message.text, "%Y-%m-%d") <= datetime.now():
                global cardData
                cardData = datetime.strptime(message.text, "%Y-%m-%d")
                await message.answer('Введите сумму затрат: ')
                botlog[0] = 5
            else: 
                await message.answer('Введите дату не больше : ' + str(datetime.now().strptime("%Y-%m-%d")))
        except ValueError:
            await message.answer('Неправильный ввод даты. Введите дату в формате 2000-05-24')
    elif botlog[0] == 5:
        try:
            int(message.text)
            global cardAmount
            cardAmount = message.text
            await message.answer("Введите описание затрат!")
            botlog[0] = 6
        except ValueError:
            await message.answer("Неправильный ввод. Введите сумму!")
    elif botlog[0] == 6:
        try:
            global cardDisc
            cardDisc = message.text
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as card:
                card.execute("SELECT * FROM salesforce.expense_card__c;")
                cardLenDo = len(card.fetchall())
          #  with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as card:
          #      card.execute("INSERT INTO salesforce.expense_card__c (card_date__c, cardkeeper__c, monthlyexpense__c, amount__c, description__c) values (%s,%s,%s,%s,%s)",(str(cardData),str(userId), str(monthlySFID),str(cardAmount),str(cardDisc)))
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as card:
                card.execute("SELECT * FROM salesforce.expense_card__c;")
                cardLenPo = len(card.fetchall())
            if cardLenDo < cardLenPo:
                await message.answer("Карточка создана!")
                botlog[0] = 0
        except ValueError:
            await message.answer("Ошибка при создании карты!")
            botlog[0] = 0



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