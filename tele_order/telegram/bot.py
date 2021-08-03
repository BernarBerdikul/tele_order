import telebot
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('telegram_bot_token')

bot = telebot.TeleBot(TOKEN)  # create a new Telegram Bot


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message)
    if message.from_user.is_bot:
        text = "Мы с ботами не работаем"
        bot.send_message(chat_id=message.from_user.id, text=text)
    text = "Рад тебя видеть друг мой"
    bot.send_message(chat_id=message.from_user.id, text=text)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    text = 'Я создан для отправки заказов, ' \
           'а не для того что бы разговаривать с вами 😐'
    bot.send_message(chat_id=message.from_user.id, text=text)
