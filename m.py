import sqlite3
import telebot
import sql3Funcs
from time import sleep
import addFuncs
import random
customerscnt = 0
flag = False
class Customer:
    
    def __init__(self, hello_message, recept, stiker):
        self.hello_message = hello_message
        self.recept = recept
        self.stiker = stiker

    def start(self, chat_id, bot):
        Keyboardin = telebot.types.InlineKeyboardMarkup()
        Keyboardin.add(
            telebot.types.InlineKeyboardButton(text='Принять заказ', callback_data='get'),
            telebot.types.InlineKeyboardButton(text='Отклонить', callback_data='dontget')
        )
        bot.send_chat_action(chat_id=chat_id, action="typing", timeout=2)
        sleep(2)
        bot.send_message(chat_id=chat_id, text=self.hello_message)
        bot.send_chat_action(chat_id=chat_id, action="choose_sticker", timeout=2)
        sleep(2)
        bot.send_sticker(chat_id=chat_id, sticker=self.stiker)
        bot.send_chat_action(chat_id=chat_id, action="typing", timeout=2)
        sleep(2)
        bot.send_message(chat_id=chat_id, text=self.recept, reply_markup=Keyboardin)
        



def genirate_recept(path, table1, table2, table3, userid):
    datafood = sql3Funcs.get_from_table(path, table1)
    datadrinks = sql3Funcs.get_from_table(path, table2)
    datadeserts = sql3Funcs.get_from_table(path, table3)
    rend = random.randint(3, 7)
    string = 'Ингридеенты:\n\n'
    r = ''
    for i in range(rend):
        a = random.randint(1, 3)
        rand = random.randint(0, len(datafood)-1)
        string += f'{datafood[rand][3]} {datafood[rand][1]} - x{a}\n'
        for i in range(a):
            r += f'{datafood[rand][0]} '
        datafood.pop(rand)
    string += '\n\nНапитки:\n\n'
    for i in range(1):
        a = random.randint(1, 3)
        rand = random.randint(0, len(datadrinks)-1)
        string += f'{datadrinks[rand][3]} {datadrinks[rand][1]} - x{a}\n'
        for i in range(a):
            r += f'{datadrinks[rand][0]} '
        datadrinks.pop(rand)
    string += '\n\nДесерты:\n\n'
    rend = random.randint(1, 3)
    for i in range(rend):
        a = random.randint(1, 3)
        rand = random.randint(0, len(datadeserts)-1)
        string += f'{datadeserts[rand][3]} {datadeserts[rand][1]} - x{a}\n'
        for i in range(a):
            r += f'{datadeserts[rand][0]} '
        datadeserts.pop(rand)
    sql3Funcs.update_table('shavuha.db', 'users', 'id', userid, castomer_recept=r)
    # with sqlite3.connect(path) as connection:
    #     cursor = connection.cursor()
    #     cursor.execute(f'''UPDATE users SET castomer_recept="{r}" 
    #                     WHERE id="{userid}"''')
    return string
    


def pay(bot, call, table1, table2):
    userid = call.from_user.id
        
    userDatad = sql3Funcs.get_from_table('shavuha.db', table1, 'id', userid)
    userDatad = list(userDatad)
    userDatad.pop(0)
    userData = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userid)
    with sqlite3.connect("shavuha.db") as connection:
        cur = connection.cursor() 
        cur.execute(f'PRAGMA table_info("{table1}")')
        column_names = [i[1] for i in cur.fetchall()]
    column_names.pop(0)
    for i in range(len(userDatad)):
        if userData[8] == column_names[i]:
            ind = i
            break
        
    mebelData = sql3Funcs.get_from_table('shavuha.db', table2, 'id', userData[8])
    balance = userData[2]
    a = userData[9]
    b = userData[8]
    amount = mebelData[2]*userData[9]
    koll = userDatad[ind]

    if balance < amount:
        bot.send_message(chat_id=call.message.chat.id, text='недостаточно монет', reply_markup=menuKeyboard)
        bot.register_next_step_handler(message=call.message, callback=time_to_begin)
        return
    sql3Funcs.update_table('shavuha.db', 'users', 'id', userid, balance=balance-amount, current_cnt=0, current='')
    with sqlite3.connect('shavuha.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f'''UPDATE {table1} SET {b}={koll+a}
                         WHERE id="{userid}"''')
    bot.send_message(chat_id=call.message.chat.id, text="Купленно", reply_markup=menuKeyboard)
    bot.register_next_step_handler(message=call.message, callback=time_to_begin)


def get_photos(user):
    user_photos = bot.get_user_profile_photos(user)
    user_photos = user_photos.photos
    photos_ids = []
    for photo in user_photos:
        photos_ids.append(photo[0].file_id)
    return photos_ids


def chek(name, id):
    if name == 'last':
        return sql3Funcs.get_from_table('shavuha.db', 'users_aksii', 'id', id)[3] == 1
    elif name == 'three':
        return sql3Funcs.get_from_table('shavuha.db', 'users_aksii', 'id', id)[2] == 1
    elif name == 'dice':
        return sql3Funcs.get_from_table('shavuha.db', 'users_aksii', 'id', id)[1] == 1
    
    

aksiiKeyboardin = telebot.types.InlineKeyboardMarkup()
aksiiKeyboardin.add(
    telebot.types.InlineKeyboardButton(text='Отменить акции', callback_data='del'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)
menuKeyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
menuKeyboard.add(
    telebot.types.KeyboardButton(text='Личные данные'),
    telebot.types.KeyboardButton(text='Магазин'),
    telebot.types.KeyboardButton(text='Инвентарь'),
    telebot.types.KeyboardButton(text='Помощь'),
    telebot.types.KeyboardButton(text='Начать')
)

shop_keyboard = telebot.types.InlineKeyboardMarkup()
shop_keyboard.add(
    telebot.types.InlineKeyboardButton(text='Продукты', callback_data='prodacts'),
    telebot.types.InlineKeyboardButton(text='Интерьер', callback_data='interer'),
    telebot.types.InlineKeyboardButton(text='Акции', callback_data='akcii'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)

in_keyboard = telebot.types.InlineKeyboardMarkup()
in_keyboard.add(
    telebot.types.InlineKeyboardButton(text='Продукты', callback_data='seeprodacts'),
    telebot.types.InlineKeyboardButton(text='Интерьер', callback_data='seeinterer'),
    telebot.types.InlineKeyboardButton(text='Акции', callback_data='seeakcii'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)

shop_keyboard_razdel = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel.add(
    telebot.types.InlineKeyboardButton(text='Напитки', callback_data='drinks'),
    telebot.types.InlineKeyboardButton(text='Десерты', callback_data='deserts'),
    telebot.types.InlineKeyboardButton(text='Еда', callback_data='food'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)

shop_keyboard_razdel_food = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel_food.add(
    telebot.types.InlineKeyboardButton(text='🍅-5₽', callback_data='tomato'),
    telebot.types.InlineKeyboardButton(text='🥔-5₽', callback_data='potato'),
    telebot.types.InlineKeyboardButton(text='🥒-10₽', callback_data='cucumber'),
    telebot.types.InlineKeyboardButton(text='🍆-5₽', callback_data='eggplant'),
    telebot.types.InlineKeyboardButton(text='🥕-5₽', callback_data='carrot'),
    telebot.types.InlineKeyboardButton(text='🌶️-10₽', callback_data='pepper'),
    telebot.types.InlineKeyboardButton(text='🥬-5₽', callback_data='salad_greens'),
    telebot.types.InlineKeyboardButton(text='🧄-5₽', callback_data='garlic'),
    telebot.types.InlineKeyboardButton(text='🧅-10₽', callback_data='onion'),
    telebot.types.InlineKeyboardButton(text='🥓-10₽', callback_data='bacon'),
    telebot.types.InlineKeyboardButton(text='🍖-15₽', callback_data='pork'),
    telebot.types.InlineKeyboardButton(text='🍗-15₽', callback_data='chicken'),
    telebot.types.InlineKeyboardButton(text='🧀-15₽', callback_data='cheese'),
    telebot.types.InlineKeyboardButton(text='🧂-5₽', callback_data='salt'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)
next_customer = telebot.types.InlineKeyboardMarkup()
next_customer.add(
    telebot.types.InlineKeyboardButton(text='Дальше', callback_data='next_c'),
)
shop_keyboard_razdel_food_game = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel_food_game.add(
    telebot.types.InlineKeyboardButton(text='🍅', callback_data='tomato'),
    telebot.types.InlineKeyboardButton(text='🥔', callback_data='potato'),
    telebot.types.InlineKeyboardButton(text='🥒', callback_data='cucumber'),
    telebot.types.InlineKeyboardButton(text='🍆', callback_data='eggplant'),
    telebot.types.InlineKeyboardButton(text='🥕', callback_data='carrot'),
    telebot.types.InlineKeyboardButton(text='🌶️', callback_data='pepper'),
    telebot.types.InlineKeyboardButton(text='🥬', callback_data='salad_greens'),
    telebot.types.InlineKeyboardButton(text='🧄', callback_data='garlic'),
    telebot.types.InlineKeyboardButton(text='🧅', callback_data='onion'),
    telebot.types.InlineKeyboardButton(text='🥓', callback_data='bacon'),
    telebot.types.InlineKeyboardButton(text='🍖', callback_data='pork'),
    telebot.types.InlineKeyboardButton(text='🍗', callback_data='chicken'),
    telebot.types.InlineKeyboardButton(text='🧀', callback_data='cheese'),
    telebot.types.InlineKeyboardButton(text='🧂', callback_data='salt'),
    telebot.types.InlineKeyboardButton(text='Дальше', callback_data='next')
)

shop_keyboard_razdel_drinks = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel_drinks.add(
    telebot.types.InlineKeyboardButton(text='☕️-10₽', callback_data='tea'),
    telebot.types.InlineKeyboardButton(text='🥤-15₽', callback_data='soda'),
    telebot.types.InlineKeyboardButton(text='🧃-15₽', callback_data='juice'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)

shop_keyboard_razdel_drinks_game = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel_drinks_game.add(
    telebot.types.InlineKeyboardButton(text='☕️', callback_data='tea'),
    telebot.types.InlineKeyboardButton(text='🥤', callback_data='soda'),
    telebot.types.InlineKeyboardButton(text='🧃', callback_data='juice'),
    telebot.types.InlineKeyboardButton(text='Дальше', callback_data='nextd')
)

shop_keyboard_razdel_deserts = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel_deserts.add(
    telebot.types.InlineKeyboardButton(text='🍦-20₽', callback_data='ice_cream'),
    telebot.types.InlineKeyboardButton(text='🧁-25₽', callback_data='cake'),
    telebot.types.InlineKeyboardButton(text='🍰-25₽', callback_data='pancake'),
    telebot.types.InlineKeyboardButton(text='🍭-15₽', callback_data='sweets'),
    telebot.types.InlineKeyboardButton(text='🍫-20₽', callback_data='chocolate'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)

shop_keyboard_razdel_deserts_game = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel_deserts_game.add(
    telebot.types.InlineKeyboardButton(text='🍦', callback_data='ice_cream'),
    telebot.types.InlineKeyboardButton(text='🧁', callback_data='cake'),
    telebot.types.InlineKeyboardButton(text='🍰', callback_data='pancake'),
    telebot.types.InlineKeyboardButton(text='🍭', callback_data='sweets'),
    telebot.types.InlineKeyboardButton(text='🍫', callback_data='chocolate'),
    telebot.types.InlineKeyboardButton(text='Завершить', callback_data='end_game')
)

shop_keyboard_razdel_interier = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel_interier.add(
    telebot.types.InlineKeyboardButton(text='📻-100₽', callback_data='radio'),
    telebot.types.InlineKeyboardButton(text='🕰️-500₽', callback_data='clock'),
    telebot.types.InlineKeyboardButton(text='🔮-2000₽', callback_data='magic_style_decor'),
    telebot.types.InlineKeyboardButton(text='💡-500₽', callback_data='lighting'),
    telebot.types.InlineKeyboardButton(text='🖼️-900₽', callback_data='picture'),
    telebot.types.InlineKeyboardButton(text='🪑-900₽', callback_data='chair'),
    telebot.types.InlineKeyboardButton(text='🛋️-1500₽', callback_data='sofa'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)
shop_keyboard_razdel_aksii = telebot.types.InlineKeyboardMarkup()
shop_keyboard_razdel_aksii.add(
    telebot.types.InlineKeyboardButton(text='Бросок кости', callback_data='dice'),
    telebot.types.InlineKeyboardButton(text='Три - счастливое число', callback_data='three'),
    telebot.types.InlineKeyboardButton(text='Последний гость', callback_data='last'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)
shop_keyboard_seerazdel = telebot.types.InlineKeyboardMarkup()
shop_keyboard_seerazdel.add(
    telebot.types.InlineKeyboardButton(text='Напитки', callback_data='seedrinks'),
    telebot.types.InlineKeyboardButton(text='Десерты', callback_data='seedeserts'),
    telebot.types.InlineKeyboardButton(text='Еда', callback_data='seefood'),
    telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu')
)

bot = telebot.TeleBot('6338167935:AAHo7RLEwHykLY0_EnBiMVuN4tN1tIu6EzQ')

@bot.message_handler(commands=['start'])
def start_message(message):
    id = message.from_user.id
    fName = message.from_user.first_name
    sql3Funcs.create_table('shavuha.db', 'users', id='INT', fName='TEXT',balance='REAL', days='INT', recept='TEXT', cosiness="INT", curentdice='INT',current_aksii='TEXT', current='TEXT', current_cnt="REAL", custamers="INT", castomer_recept="TEXT", badfeedbacks="INT")
    sql3Funcs.create_table('shavuha.db', 'users_food', id='INT', tomato="INT", potato="INT", cucumber="INT", eggplant="INT", carrot="INT", pepper="INT", salad_greens="INT", garlic="INT", onion="INT", bacon="INT", pork="INT", chicken="INT", cheese="INT", salt="INT")
    sql3Funcs.create_table('shavuha.db', 'users_drinks', id='INT', tea="INT", soda="INT", juice="INT")
    sql3Funcs.create_table('shavuha.db', 'users_sweets', id='INT', ice_cream="INT", cake="INT", pancake="INT", sweets="INT", chocolate="INT")
    sql3Funcs.create_table('shavuha.db', 'users_mebel', id='INT', radio="INT", clock="INT", lighting="INT", magic_style_decor="INT", picture="INT", chair="INT", sofa="INT")
    sql3Funcs.create_table('shavuha.db', 'users_aksii', id='INT', dice="INT", three="INT", last="INT")
    if sql3Funcs.get_from_table('shavuha.db', 'users', 'id', id) == None:
        sql3Funcs.insert_into_table('shavuha.db', 'users', id=id, fName=fName, balance=1000, days=0, recept='', cosiness=0, curentdice=0, current='', current_cnt=0, custamers=3, current_aksii='', castomer_recept='', badfeedbacks=0)
        sql3Funcs.insert_into_table('shavuha.db', 'users_food', id=id, tomato=0, potato=0, cucumber=0, eggplant=0, carrot=0, pepper=0, salad_greens=0, garlic=0, onion=0, bacon=0, pork=0, chicken=0, cheese=0, salt=0)
        sql3Funcs.insert_into_table('shavuha.db', 'users_drinks', id=id, tea=0, soda=0, juice=0)
        sql3Funcs.insert_into_table('shavuha.db', 'users_sweets', id=id, ice_cream=0, cake=0, pancake=0, sweets=0, chocolate=0)
        sql3Funcs.insert_into_table('shavuha.db', 'users_mebel', id=id, radio=0, clock=0, lighting=0, magic_style_decor=0, picture=0, chair=0, sofa=0)
        sql3Funcs.insert_into_table('shavuha.db', 'users_aksii', id=id, dice=0, three=0, last=0)
    bot.send_chat_action(chat_id=message.chat.id, action="choose_sticker", timeout=2)
    sleep(2)
    stiker = "CAACAgIAAxkBAAEEscNmGkI8qU6RWFs_wEXz5yumoS4imAACTxgAAr-DEEs9Nwjog3pgYjQE"
    bot.send_sticker(chat_id=message.chat.id, sticker=stiker)
    bot.send_chat_action(chat_id=message.chat.id, action="typing", timeout=4)
    sleep(4)
    bot.send_message(chat_id=message.chat.id, text="Привет, я менеждер этой шаурмичной. Говорят тебя перевели сюда т.к тебе удалось всё наладить в предыдущей точке нашей сети. Надеюсь ты сможешь помочь нам. А то клиентов совсем нет. Ну и на последок удчной работы :)", reply_markup=menuKeyboard)
    bot.register_next_step_handler(message=message, callback=time_to_begin)   
    
    
def time_to_begin(message):
    global flag
    flag = False
    bot.send_message(chat_id=message.chat.id,
                     text=f'Вы выбрали "{message.text}"',
                     reply_markup=telebot.types.ReplyKeyboardRemove())
    if message.text == "Личные данные":
        user_id = message.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', user_id)
        photos_ids = get_photos(user_id)
        if len(photos_ids)==0:
            with open("s.jpg", 'rb') as img:
                bot.send_photo(message.chat.id, img, caption=f"Имя: {userData[1]}\nДолжность: Шеф-повар\nКоличество пройденных дней: {userData[3]}\nУют: {userData[5]} (за каждые 4 единицы +1 покупатель в день)\nКолличество посетителей в день: {userData[10]}\nКолличество плохих отзывов: {userData[12]}\n\nБаланс: {userData[2]}")
        else:
            bot.send_photo(message.chat.id, photos_ids[0], caption=f"Имя: {userData[1]}\nДолжность: Шеф-повар\nКоличество пройденных дней: {userData[3]}\nУют: {userData[5]} (за каждые 4 единицы +1 покупатель в день)\nКолличество посетителей в день: {userData[10]}\nКолличество плохих отзывов: {userData[12]}\n\nБаланс: {userData[2]}")
        bot.send_message(chat_id=message.chat.id, text='переход обратно',
                         reply_markup=menuKeyboard)

        bot.register_next_step_handler(message=message, callback=time_to_begin)

    elif message.text == "Помощь":
        bot.send_message(chat_id=message.chat.id, text='Если возникли проблемы обращайтесь сюда: @Dazai_kin2',
                         reply_markup=menuKeyboard)

        bot.register_next_step_handler(message=message, callback=time_to_begin)

    elif message.text == "Инвентарь":
        with open("b.jpg", "rb") as img:
            bot.send_photo(message.chat.id, photo=img, caption="Выбирите интересующий вас раздел", reply_markup=in_keyboard)
    
    elif message.text == "Магазин":
        with open("shop.jpg", "rb") as img:
            bot.send_photo(message.chat.id, photo=img, caption="Выбирите интересующий вас раздел", reply_markup=shop_keyboard)

    elif message.text == "Начать":
        global customerscnt
        customerscnt += 1
        hello = ["Привет, можите принять мой заказ?", "Я бы хотел сделать у вас заказ", 
                "Слышал сдесь продаётся хорошая шаурма, я бы хотел заказать", 
                "З-з-здравствуйте... Эм... Немогли бы вы принять мой заказ...пожалуйса?",
                "Погодка сегодня отличная не так ли? Решил сегодня зайти к вам", "Можно сделать заказ?", 
                "Хотелось бы чего-нибуть сытного... Может это?"]
        stikers = ["CAACAgIAAxkBAAEFAoNmK85_o4Qy7SiIHUr0rBHNxyyeSQACyiMAAh-lkUreRxffd4TdhzQE",
                   "CAACAgIAAxkBAAEFAn1mK85fViEFVinGI7oFQnbPb-pd_QAC1hwAAhG0mUpJOLYV_7j3mDQE",
                   "CAACAgIAAxkBAAEFAodmK86R3qAKazNJt8wLouVO-tV-eAACkRQAAv0XyEnQiUaGlOf0gDQE",
                   "CAACAgIAAxkBAAEFAoFmK85qlur7BMP2JbbBv8l6d2hcOwACoBsAAhyjmEresf7Tn6EAAdg0BA",
                   "CAACAgIAAxkBAAEFAoVmK86LLjDnJMuStoVLEyEJ7XjEYwACDA8AAo6YoUmB6kdK8-yHrjQE",
                   "CAACAgIAAxkBAAEFAn9mK85itLf61zGU4tFyND194zFLbQACmhwAAuV_mUrI_bjZDY6OVjQE",
                   "CAACAgIAAxkBAAEE8S1mJ-2bv4_W2G6h7-PPC2sVhUJFcwACMxQAAkVgkErJrYlpm1MxmjQE"]
        recepts = genirate_recept('shavuha.db', 'food', 'drinks', 'desserts', message.from_user.id)
        rand = random.randint(0, len(hello)-1)
        customer = Customer(hello[rand], recepts, stikers[rand])
        customer.start(message.chat.id, bot)

    else:
        bot.send_message(chat_id=message.chat.id, text='к сожелению такая функция ещё не доступна :(',
                         reply_markup=menuKeyboard)

        bot.register_next_step_handler(message=message, callback=time_to_begin)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    global customerscnt
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.id)
    if call.data == 'backMainMenu':
        bot.send_message(chat_id=call.message.chat.id, text='Выберите один из пунктов меню', reply_markup=menuKeyboard)

        bot.register_next_step_handler(message=call.message, callback=time_to_begin)
    elif call.data == "prodacts":
        bot.send_message(call.message.chat.id, text="Выбирите интересующий вас раздел", reply_markup=shop_keyboard_razdel)
    elif call.data == "food":
        bot.send_message(call.message.chat.id, text="выбирите продукт", reply_markup=shop_keyboard_razdel_food)
    elif call.data == "drinks":
        bot.send_message(call.message.chat.id, text="выбирите продукт", reply_markup=shop_keyboard_razdel_drinks)
    elif call.data == "deserts":
        bot.send_message(call.message.chat.id, text="выбирите продукт", reply_markup=shop_keyboard_razdel_deserts)
    elif call.data == "interer":
        bot.send_message(call.message.chat.id, text="выбирите интерьер", reply_markup=shop_keyboard_razdel_interier)
    elif call.data == "akcii":
        bot.send_message(call.message.chat.id, text="выбирите акцию", reply_markup=shop_keyboard_razdel_aksii)
    elif call.data in addFuncs.getColumnValues('shavuha.db', 'stocks', 0):
        userId = call.from_user.id
        sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, current_aksii=call.data)
        aksiiData = sql3Funcs.get_from_table('shavuha.db', 'stocks', 'id', call.data)
        aksiiKeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        aksiiKeyboard.add(
            telebot.types.InlineKeyboardButton(text='Активировать', callback_data='addstoks'),
            telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu'),
        )
        bot.send_message(call.message.chat.id, text=f"<strong>{aksiiData[1]}</strong>\n\n{aksiiData[2]}\n+{aksiiData[3]} покупателя в день", reply_markup=aksiiKeyboard, parse_mode="HTML")
    elif call.data == 'get':
        bot.send_message(call.message.chat.id, text="Выбирайте продукты в том же порядке и количестве", reply_markup=shop_keyboard_razdel_food_game)
        global flag
        flag = True

    elif call.data == "seeprodacts":
        bot.send_message(call.message.chat.id, text="Выбирите интересующий вас раздел", reply_markup=shop_keyboard_seerazdel)

    elif call.data == "seefood":
        userId = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users_food', "id", userId)
        userData = list(userData)
        userData.pop(0)
        if max(userData) == 0 and min(userData) == 0:
            bot.send_message(chat_id=call.message.chat.id, text='пусто', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        a = ''
        with sqlite3.connect("shavuha.db") as connection:
            cur = connection.cursor() 
            cur.execute('PRAGMA table_info("users_food")')
            column_names = [i[1] for i in cur.fetchall()]
        column_names.pop(0)
        for i in range(len(userData)):
            if userData[i] != 0:
                foodData = sql3Funcs.get_from_table('shavuha.db', 'food', "id", column_names[i])
                string = f'{foodData[3]} {foodData[1]} - x{userData[i]}\n'
                a += string
        bot.send_message(chat_id=call.message.chat.id, text=a, reply_markup=menuKeyboard)
        bot.register_next_step_handler(message=call.message, callback=time_to_begin)

    elif call.data == "seeinterer":
        userId = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users_mebel', "id", userId)
        userData = list(userData)
        userData.pop(0)
        if max(userData) == 0:
            bot.send_message(chat_id=call.message.chat.id, text='пусто', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        a = ''
        with sqlite3.connect("shavuha.db") as connection:
            cur = connection.cursor() 
            cur.execute('PRAGMA table_info("users_mebel")')
            column_names = [i[1] for i in cur.fetchall()]
        column_names.pop(0)
        for i in range(len(userData)):
            if userData[i] != 0:
                foodData = sql3Funcs.get_from_table('shavuha.db', 'furniture', "id", column_names[i])
                string = f'{foodData[3]} {foodData[1]} - x{userData[i]}\n'
                a += string
        bot.send_message(chat_id=call.message.chat.id, text=a, reply_markup=menuKeyboard)
        bot.register_next_step_handler(message=call.message, callback=time_to_begin)
    elif call.data == "seeakcii":
        userId = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users_aksii', "id", userId)
        userData = list(userData)
        userData.pop(0)
        if max(userData) == 0:
            bot.send_message(chat_id=call.message.chat.id, text='пусто', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        a = ''
        with sqlite3.connect("shavuha.db") as connection:
            cur = connection.cursor() 
            cur.execute('PRAGMA table_info("users_aksii")')
            column_names = [i[1] for i in cur.fetchall()]
        column_names.pop(0)
        for i in range(len(userData)):
            if userData[i] != 0:
                foodData = sql3Funcs.get_from_table('shavuha.db', 'stocks', "id", column_names[i])
                string = f"<strong>{foodData[1]}</strong>\n\n{foodData[2]}\n+{foodData[3]} покупателя в день\n\n"
                a += string
        bot.send_message(chat_id=call.message.chat.id, text=a, reply_markup=aksiiKeyboardin, parse_mode='HTML')

    elif call.data in addFuncs.getColumnValues('shavuha.db', 'furniture', 0):
        id = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users_mebel', 'id', id)
        userData = list(userData)
        userData.pop(0)
        with sqlite3.connect("shavuha.db") as connection:
            cur = connection.cursor() 
            cur.execute('PRAGMA table_info("users_mebel")')
            column_names = [i[1] for i in cur.fetchall()]
        column_names.pop(0)
        for i in range(len(userData)):
            if call.data == column_names[i]:
                index = i
                break
        if userData[index] == 1:
            bot.send_message(chat_id=call.message.chat.id, text='У вас уже это есть', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        userid = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userid)
        mebelData = sql3Funcs.get_from_table('shavuha.db', 'furniture', 'id', call.data)
        balance = userData[2]
        amount = mebelData[2]
        castomers = userData[10]
        userC = userData[5]
        mebelC = mebelData[4]
        if balance < amount:
            bot.send_message(chat_id=call.message.chat.id, text='недостаточно монет', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        sql3Funcs.update_table('shavuha.db', 'users', 'id', userid, balance=balance-amount, cosiness=(userC+mebelC)%4, custamers=castomers+(userC+mebelC)//4)
        with sqlite3.connect('shavuha.db') as connection:
            cursor = connection.cursor()
            cursor.execute(f'''UPDATE users_mebel SET {call.data}=1
                            WHERE id="{id}"''')
        bot.send_message(chat_id=call.message.chat.id, text="Купленно", reply_markup=menuKeyboard)
        bot.register_next_step_handler(message=call.message, callback=time_to_begin)


    elif call.data in addFuncs.getColumnValues('shavuha.db', 'drinks', 0):
        userId = call.from_user.id
        if (flag):
            userData = sql3Funcs.get_from_table('shavuha.db', 'users', "id", userId)
            recept = userData[4]
            sql3Funcs.update_table('shavuha.db', 'users', "id", userId, recept=recept+call.data+" ")
            userDatad = sql3Funcs.get_from_table('shavuha.db', "users_drinks", 'id', userId)
            userDatad = list(userDatad)
            userDatad.pop(0)
            with sqlite3.connect("shavuha.db") as connection:
                cur = connection.cursor() 
                cur.execute(f'PRAGMA table_info("users_drinks")')
                column_names = [i[1] for i in cur.fetchall()]
            column_names.pop(0)
            for i in range(len(userDatad)):
                if call.data == column_names[i]:
                    ind = i
                    break
            with sqlite3.connect('shavuha.db') as connection:
                cursor = connection.cursor()
                cursor.execute(f'''UPDATE {"users_drinks"} SET {call.data}={userDatad[ind]-1}
                         WHERE id="{userId}"''')
            bot.send_message(call.message.chat.id, text="Добавлено", reply_markup=shop_keyboard_razdel_drinks_game)
            return


        id = call.from_user.id
        sql3Funcs.update_table('shavuha.db', 'users', 'id', id, current=call.data)
        kollKeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        kollKeyboard.add(
            telebot.types.InlineKeyboardButton(text='5', callback_data="5"),
            telebot.types.InlineKeyboardButton(text='20', callback_data="20"),
            telebot.types.InlineKeyboardButton(text='40', callback_data="40"),
            telebot.types.InlineKeyboardButton(text='50', callback_data="50"),
            telebot.types.InlineKeyboardButton(text='60', callback_data="60"),
            telebot.types.InlineKeyboardButton(text='70', callback_data="70"),
            telebot.types.InlineKeyboardButton(text='80', callback_data="80"),
            telebot.types.InlineKeyboardButton(text='90', callback_data="90"),
        )
        bot.send_message(chat_id=call.message.chat.id, text='выбирите количество товара', reply_markup=kollKeyboard)
    elif call.data in addFuncs.getColumnValues('shavuha.db', 'desserts', 0):
        userId = call.from_user.id
        if (flag):
            userData = sql3Funcs.get_from_table('shavuha.db', 'users', "id", userId)
            recept = userData[4]
            sql3Funcs.update_table('shavuha.db', 'users', "id", userId, recept=recept+call.data+" ")
            userDatad = sql3Funcs.get_from_table('shavuha.db', "users_sweets", 'id', userId)
            userDatad = list(userDatad)
            userDatad.pop(0)
            with sqlite3.connect("shavuha.db") as connection:
                cur = connection.cursor() 
                cur.execute(f'PRAGMA table_info("users_sweets")')
                column_names = [i[1] for i in cur.fetchall()]
            column_names.pop(0)
            for i in range(len(userDatad)):
                if call.data == column_names[i]:
                    ind = i
                    break
            with sqlite3.connect('shavuha.db') as connection:
                cursor = connection.cursor()
                cursor.execute(f'''UPDATE {"users_sweets"} SET {call.data}={userDatad[ind]-1}
                         WHERE id="{userId}"''')
            bot.send_message(call.message.chat.id, text="Добавлено", reply_markup=shop_keyboard_razdel_deserts_game)
            return


        id = call.from_user.id
        sql3Funcs.update_table('shavuha.db', 'users', 'id', id, current=call.data)
        kollKeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        kollKeyboard.add(
            telebot.types.InlineKeyboardButton(text='5', callback_data="5"),
            telebot.types.InlineKeyboardButton(text='20', callback_data="20"),
            telebot.types.InlineKeyboardButton(text='40', callback_data="40"),
            telebot.types.InlineKeyboardButton(text='50', callback_data="50"),
            telebot.types.InlineKeyboardButton(text='60', callback_data="60"),
            telebot.types.InlineKeyboardButton(text='70', callback_data="70"),
            telebot.types.InlineKeyboardButton(text='80', callback_data="80"),
            telebot.types.InlineKeyboardButton(text='90', callback_data="90"),
        )
        bot.send_message(chat_id=call.message.chat.id, text='выбирите количество товара', reply_markup=kollKeyboard)
    elif call.data in addFuncs.getColumnValues('shavuha.db', 'food', 0):
        userId = call.from_user.id
        if (flag):
            userData = sql3Funcs.get_from_table('shavuha.db', 'users', "id", userId)
            recept = userData[4]
            sql3Funcs.update_table('shavuha.db', 'users', "id", userId, recept=recept+call.data+" ")
            userDatad = sql3Funcs.get_from_table('shavuha.db', "users_food", 'id', userId)
            userDatad = list(userDatad)
            userDatad.pop(0)
            with sqlite3.connect("shavuha.db") as connection:
                cur = connection.cursor() 
                cur.execute(f'PRAGMA table_info("users_food")')
                column_names = [i[1] for i in cur.fetchall()]
            column_names.pop(0)
            for i in range(len(userDatad)):
                if call.data == column_names[i]:
                    ind = i
                    break
            with sqlite3.connect('shavuha.db') as connection:
                cursor = connection.cursor()
                cursor.execute(f'''UPDATE {'users_food'} SET {call.data}={userDatad[ind]-1}
                         WHERE id="{userId}"''')
            bot.send_message(call.message.chat.id, text="Добавлено", reply_markup=shop_keyboard_razdel_food_game)
            return

        id = call.from_user.id
        sql3Funcs.update_table('shavuha.db', 'users', 'id', id, current=call.data)
        kollKeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        kollKeyboard.add(
            telebot.types.InlineKeyboardButton(text='5', callback_data="5"),
            telebot.types.InlineKeyboardButton(text='20', callback_data="20"),
            telebot.types.InlineKeyboardButton(text='40', callback_data="40"),
            telebot.types.InlineKeyboardButton(text='50', callback_data="50"),
            telebot.types.InlineKeyboardButton(text='60', callback_data="60"),
            telebot.types.InlineKeyboardButton(text='70', callback_data="70"),
            telebot.types.InlineKeyboardButton(text='80', callback_data="80"),
            telebot.types.InlineKeyboardButton(text='90', callback_data="90"),
        )
        bot.send_message(chat_id=call.message.chat.id, text='выбирите количество товара', reply_markup=kollKeyboard)
    elif call.data in ["5", "20", "40", "50", "60", "70", "80", "90"]:
        id = call.from_user.id
        sql3Funcs.update_table('shavuha.db', 'users', 'id', id, current_cnt=call.data)
        kollKeyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
        kollKeyboard.add(
            telebot.types.InlineKeyboardButton(text='Оплатить', callback_data='pay'),
            telebot.types.InlineKeyboardButton(text='Главное меню', callback_data='backMainMenu'),
        )
        bot.send_message(chat_id=call.message.chat.id, text='выбирите действие', reply_markup=kollKeyboard)
    elif call.data == 'pay':
        userid = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userid)
        if sql3Funcs.get_from_table('shavuha.db', 'drinks', 'id', userData[8]) != None:
            pay(bot, call, 'users_drinks', 'drinks')
        elif sql3Funcs.get_from_table('shavuha.db', 'food', 'id', userData[8]) != None:
            pay(bot, call, 'users_food', 'food')
        else:
            pay(bot, call, 'users_sweets', 'desserts')
        
    elif call.data == "next":
        bot.send_message(call.message.chat.id, text="Выбирайте напитки", reply_markup=shop_keyboard_razdel_drinks_game)

    elif call.data == "nextd":
        bot.send_message(call.message.chat.id, text="Выбирайте десерты", reply_markup=shop_keyboard_razdel_deserts_game)

    elif call.data == "seedrinks":
        userId = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users_drinks', "id", userId)
        userData = list(userData)
        userData.pop(0)
        if max(userData) == 0 and min(userData) == 0:
            bot.send_message(chat_id=call.message.chat.id, text='пусто', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        a = ''
        with sqlite3.connect("shavuha.db") as connection:
            cur = connection.cursor() 
            cur.execute('PRAGMA table_info("users_drinks")')
            column_names = [i[1] for i in cur.fetchall()]
        column_names.pop(0)
        for i in range(len(userData)):
            if userData[i] != 0:
                foodData = sql3Funcs.get_from_table('shavuha.db', 'drinks', "id", column_names[i])
                string = f'{foodData[3]} {foodData[1]} - x{userData[i]}\n'
                a += string
        bot.send_message(chat_id=call.message.chat.id, text=a, reply_markup=menuKeyboard)
        bot.register_next_step_handler(message=call.message, callback=time_to_begin)
        
    elif call.data == "seedeserts":
        userId = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users_sweets', "id", userId)
        userData = list(userData)
        userData.pop(0)
        if max(userData) == 0 and min(userData) == 0:
            bot.send_message(chat_id=call.message.chat.id, text='пусто', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        a = ''
        with sqlite3.connect("shavuha.db") as connection:
            cur = connection.cursor() 
            cur.execute('PRAGMA table_info("users_sweets")')
            column_names = [i[1] for i in cur.fetchall()]
        column_names.pop(0)
        for i in range(len(userData)):
            if userData[i] != 0:
                foodData = sql3Funcs.get_from_table('shavuha.db', 'desserts', "id", column_names[i])
                string = f'{foodData[3]} {foodData[1]} - x{userData[i]}\n'
                a += string
        bot.send_message(chat_id=call.message.chat.id, text=a, reply_markup=menuKeyboard)
        bot.register_next_step_handler(message=call.message, callback=time_to_begin)
    elif call.data == "del":
        userId = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users_aksii', "id", userId)
        userData = list(userData)
        userData.pop(0)
        userData2 = sql3Funcs.get_from_table('shavuha.db', 'users', "id", userId)
        a = 0
        with sqlite3.connect("shavuha.db") as connection:
            cur = connection.cursor() 
            cur.execute('PRAGMA table_info("users_aksii")')
            column_names = [i[1] for i in cur.fetchall()]
        column_names.pop(0)
        for i in range(len(userData)):
            if userData[i] != 0:
                foodData = sql3Funcs.get_from_table('shavuha.db', 'stocks', "id", column_names[i])
                
                a += foodData[3]
        sql3Funcs.update_table('shavuha.db', 'users_aksii', "id", userId, dice=0, three=0, last=0)
        sql3Funcs.update_table('shavuha.db', 'users', "id", userId, custamers=userData2[10]-a)
        bot.send_message(chat_id=call.message.chat.id, text="Акции удалены, включить их снова можно в магазине", reply_markup=menuKeyboard)
        bot.register_next_step_handler(message=call.message, callback=time_to_begin)
    elif call.data == "addstoks":
        userId = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users', "id", userId)
        curent = userData[7]
        useraksii = sql3Funcs.get_from_table('shavuha.db', 'users_aksii', 'id', userId)
        useraksii = list(useraksii)
        useraksii.pop(0)
        with sqlite3.connect("shavuha.db") as connection:
            cur = connection.cursor() 
            cur.execute('PRAGMA table_info("users_aksii")')
            column_names = [i[1] for i in cur.fetchall()]
        column_names.pop(0)
        for i in range(len(useraksii)):
            if curent == column_names[i]:
                index = i
                break
        if useraksii[index] == 1:
            bot.send_message(chat_id=call.message.chat.id, text='У вас уже это есть', reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        if curent == "dice":
            sql3Funcs.update_table('shavuha.db', 'users_aksii', 'id', userId, dice=1)
        elif curent == "three":
            sql3Funcs.update_table('shavuha.db', 'users_aksii', 'id', userId, three=1)
        else:
            sql3Funcs.update_table('shavuha.db', 'users_aksii', 'id', userId, last=1)
        c = sql3Funcs.get_from_table('shavuha.db', 'stocks', "id", curent)
        j = c[3] + userData[10]
        sql3Funcs.update_table('shavuha.db', 'users', "id", userId, custamers=j)
        bot.send_message(chat_id=call.message.chat.id, text="Акция активирована", reply_markup=menuKeyboard)
        bot.register_next_step_handler(message=call.message, callback=time_to_begin)
    elif call.data == "end_game":
        flag = False
        userId = call.from_user.id
        userData = sql3Funcs.get_from_table('shavuha.db', 'users', "id", userId)
        recept = addFuncs.toListBySep(userData[4], " ")
        customer_recept = addFuncs.toListBySep(userData[11], " ")
        true = 0
        cnt = 0

        while len(recept) != len(customer_recept):
            if len(recept) < len(customer_recept):
                recept.append("p")
            else:
                recept.pop(-1)
        for i in range(len(recept)):
            if recept[i] == customer_recept[i]:
                true += 1
            cnt += 1
        totall = true/cnt * 100
        if chek("last", userId) and customerscnt == sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userId)[10]:
            bot.send_message(chat_id=call.message.chat.id, text="О сегодня я последний покупатель!", reply_markup=next_customer)
            sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, recept='')
            if totall <= 40:
                bad = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userId)[12]
                sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, badfeedbacks=bad+1)
            return
        elif chek("three", userId) and customerscnt % 3 == 0:
            bot.send_message(chat_id=call.message.chat.id, text="О сегодня я третий покупатель!", reply_markup=next_customer)
            sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, recept='')
            if totall <= 40:
                bad = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userId)[12]
                sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, badfeedbacks=bad+1)
            return
        elif chek("dice", userId):
            msg = bot.send_dice(call.message.chat.id)
            msg = msg.dice.value
            sleep(4)
            if msg == 6:
                sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, recept='')
                if totall <= 40:
                    bad = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userId)[12]
                    sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, badfeedbacks=bad+1)
                bot.send_message(chat_id=call.message.chat.id, text="Мне сегодня повезло!", reply_markup=next_customer)
                return
        
        if totall >= 70:
            balance = userData[2]
            sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, balance=balance+700, recept='')
            bot.send_message(chat_id=call.message.chat.id, text="Всё отлично!", reply_markup=next_customer)
        elif totall < 70 and totall > 40:
            balance = userData[2]
            sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, balance=balance+400, recept='')
            bot.send_message(chat_id=call.message.chat.id, text="Не плохо", reply_markup=next_customer)
        else:
            balance = userData[2]
            bad = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userId)[12]
            sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, balance=balance+200, recept='', badfeedbacks=bad+1)
            bot.send_message(chat_id=call.message.chat.id, text="Всё ужасно!", reply_markup=next_customer)
    elif call.data == 'dontget':
        bot.send_message(chat_id=call.message.chat.id, text="Жаль", reply_markup=next_customer)
    elif call.data == "next_c":
        userId = call.from_user.id
        if customerscnt == sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userId)[10]:
            customerscnt = 0
            userData = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', call.from_user.id)
            sql3Funcs.update_table('shavuha.db', 'users', 'id', call.from_user.id, days = userData[3]+1)
            rand = random.randint(1, 10)
            if rand == 2 or rand == 1 or sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userId)[12] == 10:
                bot.send_message(chat_id=call.message.chat.id, text="Событие: Комиссия решила устроить проверку этому кафе")
                sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, badfeedbacks=0)
                foodData = sql3Funcs.get_from_table('shavuha.db', 'users_food', 'id', userId)
                drinksData = sql3Funcs.get_from_table('shavuha.db', 'users_drinks', 'id', userId)
                sweetsData = sql3Funcs.get_from_table('shavuha.db', 'users_sweets', 'id', userId)
                with sqlite3.connect("shavuha.db") as connection:
                    cur = connection.cursor() 
                    cur.execute(f'PRAGMA table_info("users_sweets")')
                    sweetscolumn_names = [i[1] for i in cur.fetchall()]
                with sqlite3.connect("shavuha.db") as connection:
                    cur = connection.cursor() 
                    cur.execute(f'PRAGMA table_info("users_food")')
                    foodcolumn_names = [i[1] for i in cur.fetchall()]
                with sqlite3.connect("shavuha.db") as connection:
                    cur = connection.cursor() 
                    cur.execute('PRAGMA table_info("users_drinks")')
                    drinkscolumn_names = [i[1] for i in cur.fetchall()]
                flag = False
                for i in range(len(foodData)):
                    if foodData[i] < 0:
                        with sqlite3.connect("shavuha.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute(f'''UPDATE users_food SET {foodcolumn_names[i]}=0 
                                            WHERE id="{userId}"''')
                        flag = True
                for i in range(len(drinksData)):
                    
                    if drinksData[i] < 0:
                        with sqlite3.connect("shavuha.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute(f'''UPDATE users_drinks SET {drinkscolumn_names[i]}=0
                                            WHERE id="{userId}"''')
                        flag = True
                for i in range(len(sweetsData)):
                    if sweetsData[i] < 0:
                        with sqlite3.connect("shavuha.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute(f'''UPDATE users_sweets SET {sweetscolumn_names[i]}=0
                                            WHERE id="{userId}"''')
                        flag = True
                if flag:
                    bot.send_message(chat_id=call.message.chat.id, text="Комиссия выявила нарушения, штраф: 800 монет")
                    balance = sql3Funcs.get_from_table('shavuha.db', 'users', 'id', userId)[2]
                    sql3Funcs.update_table('shavuha.db', 'users', 'id', userId, balance=balance-800)
                else:
                    bot.send_message(chat_id=call.message.chat.id, text="Проверка завершна, всё в порядке")

            bot.send_message(chat_id=call.message.chat.id, text="День завершён", reply_markup=menuKeyboard)
            bot.register_next_step_handler(message=call.message, callback=time_to_begin)
            return
        hello = ["Привет, можите принять мой заказ?", "Я бы хотел сделать у вас заказ", 
                "Слышал сдесь продаётся хорошая шаурма, я бы хотел заказать", 
                "З-з-здравствуйте... Эм... Немогли бы вы принять мой заказ...пожалуйса?",
                "Погодка сегодня отличная не так ли? Решил сегодня зайти к вам", "Можно сделать заказ?", 
                "Хотелось бы чего-нибуть сытного... Может это?"]
        stikers = ["CAACAgIAAxkBAAEFAoNmK85_o4Qy7SiIHUr0rBHNxyyeSQACyiMAAh-lkUreRxffd4TdhzQE",
                   "CAACAgIAAxkBAAEFAn1mK85fViEFVinGI7oFQnbPb-pd_QAC1hwAAhG0mUpJOLYV_7j3mDQE",
                   "CAACAgIAAxkBAAEFAodmK86R3qAKazNJt8wLouVO-tV-eAACkRQAAv0XyEnQiUaGlOf0gDQE",
                   "CAACAgIAAxkBAAEFAoFmK85qlur7BMP2JbbBv8l6d2hcOwACoBsAAhyjmEresf7Tn6EAAdg0BA",
                   "CAACAgIAAxkBAAEFAoVmK86LLjDnJMuStoVLEyEJ7XjEYwACDA8AAo6YoUmB6kdK8-yHrjQE",
                   "CAACAgIAAxkBAAEFAn9mK85itLf61zGU4tFyND194zFLbQACmhwAAuV_mUrI_bjZDY6OVjQE",
                   "CAACAgIAAxkBAAEE8S1mJ-2bv4_W2G6h7-PPC2sVhUJFcwACMxQAAkVgkErJrYlpm1MxmjQE"]
        recepts = genirate_recept('shavuha.db', 'food', 'drinks', 'desserts', call.from_user.id)
        rand = random.randint(0, len(hello)-1)
        customer = Customer(hello[rand], recepts, stikers[rand])
        customer.start(call.message.chat.id, bot)
        customerscnt += 1
        


bot.polling(none_stop=True, interval=0)
