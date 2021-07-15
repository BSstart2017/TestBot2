from flask import Flask, request
import telebot

bot = telebot.TeleBot('1835876628:AAGmblR_mTmz-p-7QpB7g-QRehHaYFpN3Ig')
bot.set_webhook(url="https://andreewtelegabot.herokuapp.com/")
app = Flask(__name__)


@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok"


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, 'Hello!')


if __name__ == "__main__":
    app.run()