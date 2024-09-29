import telebot
import sql3Funcs
import addFuncs



@bot.message_handler(commands=['start'])
def start_message(message):
    Keyboardin = telebot.types.InlineKeyboardMarkup()
    Keyboardin.add(
        telebot.types.InlineKeyboardButton(text='Купить билет', callback_data='get'),
        telebot.types.InlineKeyboardButton(text='Оставить заметку', callback_data='dontget')
    )

    bot.send_message(message.chat.id, 'Привет! Выберите опцию:', reply_markup=Keyboardin)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'get':
        bot.send_message(call.message.chat.id, 'Вы выбрали купить билет.')
    elif call.data == 'dontget':
        bot.send_message(call.message.chat.id, 'Вы выбрали оставить заметку.')


bot = telebot.TeleBot('7601076279:AAFi-DTUWaSVg1d9WBlcMPLYLHKlJxg-1yc')


bot.polling(one_stop=True, interval=0)
