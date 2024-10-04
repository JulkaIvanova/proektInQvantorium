import telebot
import AllClasses
from cinemaSession import CinemaSession
from session import Session
import sql3Funcs
from time import sleep

bot = telebot.TeleBot("7601076279:AAFi-DTUWaSVg1d9WBlcMPLYLHKlJxg-1yc")


sessions_list = {}

@bot.message_handler()
def test_message(message):
    session = sessions_list.get(message.chat.id)
    if session == None:
        session = CinemaSession(message.from_user, message.chat.id, bot)
        sessions_list[message.chat.id] = session
    session.onMessage(message)


while True:
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as error:
        print(error)
        sleep(15)
