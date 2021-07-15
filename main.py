import telebot
bot = telebot.TeleBot('1835876628:AAGmblR_mTmz-p-7QpB7g-QRehHaYFpN3Ig')
  
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Введите пароль")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /start.")




bot.polling(none_stop=True)