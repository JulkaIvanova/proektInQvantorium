from AllClasses import Cinema, CinemaHall, Movies
from session import Session
import telebot
import webbrowser
import sql3Funcs
import uuid

SI_START = 0
SI_MAIN_MENU = 1
SI_ORDER = 2
SI_ORDER_MENU = 3
SI_BOOK_WITH_HELP = 4
SI_BOOK_MANUAL = 5
SI_CHOOSE_FILM = 6
SI_CHOOSE_HALL = 7
SI_CHOOSE_HALL_DONE = 8
SI_CHOOSE_TIME = 9
SI_CHOOSE_TIME_DONE = 10
SI_CHOOSE_TIME_OK = 11
SI_WEBSITE = 12
SI_SEEBOOK = 13
SI_DELBOOK = 14
SI_DELBOOKSTEPTWO = 15
SI_CONTUNIE_CHOOSE = 16
SI_CHOOSE_PLACE = 17
SI_CONTUNIE_SIET = 18

def chek(a, b):
        for i in b:
            if i[1] == a[0] and i[2] == a[1] and i[3] == a[2] and i[4] == a[3]:
                return True
        return False 


class CinemaSession(Session):
    def __init__(self, user, chatid, bot: telebot.TeleBot):
        super().__init__(user, chatid, bot)

        a = [
            Movies("Майор Гром: Трудное детсво", 100),
            Movies("Преступление и наказание", 110),
            Movies("Аватар2", 170),
        ]
        b = [
            Movies("Преступление и наказание", 110),
            Movies("Аватар2", 170),
        ]
        c = [
            Movies("Астрал", 98),
            Movies("Душа", 106),
            Movies("Лёд 2", 132),
            Movies("Мулан", 115),
            Movies("Троли мировой тур", 91),
        ]
        self._cinema = Cinema(
            "Кинолюб",
            [
                CinemaHall(10, 10, "A", {"09:00": a[0], "11:00": a[1], "14:00": a[2]}),
                CinemaHall(5, 10, "B", {"09:00": b[0], "11:00": b[0], "14:00": b[1]}),
                CinemaHall(8, 15, "C", {"09:00": c[0], "11:00": c[1], "13:00": c[2], "15:30":c[3], "18:00":c[4]}),
            ],
        )

        self.bookedSeates = sql3Funcs.get_from_table("tiket.db", "books")
        self.film = ""
        self.hall = ""

        self.menuKeyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        self.menuKeyboard.add(
            telebot.types.KeyboardButton(text="Забронировать место"),
            telebot.types.KeyboardButton(text="Отменить бронь"),
            telebot.types.KeyboardButton(text="Наш веб-сайт"),
            telebot.types.KeyboardButton(text="Посмотреть все активные заказы"),
        )

        self.state_machine.addState(SI_START, self.state_start)
        self.state_machine.addState(SI_MAIN_MENU, self.state_main_menu)
        self.state_machine.addState(SI_ORDER, self.state_order)
        self.state_machine.addState(SI_ORDER_MENU, self.state_order_menu)
        self.state_machine.addState(SI_BOOK_WITH_HELP, self.state_book_with_help)
        self.state_machine.addState(SI_BOOK_MANUAL, self.state_book_manual)
        self.state_machine.addState(SI_CHOOSE_FILM, self.state_choose_film)
        self.state_machine.addState(SI_CHOOSE_HALL, self.state_choose_hall)
        self.state_machine.addState(SI_CHOOSE_HALL_DONE, self.state_choose_hall_done)
        self.state_machine.addState(SI_CHOOSE_TIME, self.state_choose_time)
        self.state_machine.addState(SI_CHOOSE_TIME_DONE, self.state_choose_time_done)
        self.state_machine.addState(SI_CHOOSE_TIME_OK, self.state_choose_time_ok)
        self.state_machine.addState(SI_WEBSITE, self.state_web)
        self.state_machine.addState(SI_SEEBOOK, self.state_see_book)
        self.state_machine.addState(SI_DELBOOK, self.state_del_book)
        self.state_machine.addState(SI_DELBOOKSTEPTWO, self.state_del_book_step_two)
        self.state_machine.addState(SI_CONTUNIE_CHOOSE, self.state_contunie_choose_place)
        self.state_machine.addState(SI_CHOOSE_PLACE, self.state_see_sites)
        self.state_machine.addState(SI_CONTUNIE_SIET, self.state_contunie_choose_site)

    def state_start(self, message: telebot.types.Message, stateid):
        userid = self.user.id
        fName = self.user.first_name

        sql3Funcs.create_table("tiket.db", "users", id="INT", fName="TEXT")
        sql3Funcs.create_table(
            "tiket.db",
            "books",
            uuid="TEXT",
            row="INT",
            sits="INT",
            move="TEXT",
            time="TEXT",
            id="INT",
        )

        if sql3Funcs.get_from_table("tiket.db", "users", "id", userid) == None:
            sql3Funcs.insert_into_table("tiket.db", "users", id=userid, fName=fName)

        userData = sql3Funcs.get_from_table("tiket.db", "users", "id", userid)

        with open("start.jpg", "rb") as img:
            self.bot.send_photo(
                chat_id=self.id,
                photo=img,
                caption=f"Добро пожаловать, {userData[1]}. Эта система поможет вам забронировать место на киносеанс",
                reply_markup=self.menuKeyboard,
            )

        return SI_MAIN_MENU

    def state_main_menu(self, message: telebot.types.Message, stateid):
        if message.text == "Забронировать место":
            return (SI_ORDER, True)
        elif message.text == "Наш веб-сайт":
            return(SI_WEBSITE, True)
        elif message.text == "Посмотреть все активные заказы":
            return(SI_SEEBOOK, True)
        elif message.text == "Отменить бронь":
            return(SI_DELBOOK, True)
        return (SI_START, True)
    
    def state_web(self, message: telebot.types.Message, stateid):
        self.bot.send_message(chat_id=message.chat.id, text="https://julkaivanova.github.io/Cinema.github.io/")
        return (SI_START, True)
    
    def state_see_book(self, message: telebot.types.Message, stateid):
        AllBooks = sql3Funcs.get_from_table("tiket.db", "books")
        userID = self.user.id
        userBooks = ""
        for book in AllBooks:
            if book[5] == userID:
                userBooks += f"{book[0]}\nРяд: {book[1] + 1}\nМесто: {book[2] + 1}\nФильм: {book[3]}\nНачало: {book[4]}\n"
        if len(userBooks) == 0:
            self.bot.send_message(chat_id=self.id, text="Пока что нет действительных броней")
        else:
            self.bot.send_message(chat_id=self.id, text=f"{userBooks[:-1]}")
        return (SI_START, True)

    def state_del_book(self, message: telebot.types.Message, stateid):
        AllBooks = sql3Funcs.get_from_table("tiket.db", "books")
        userID = self.user.id
        self.userBooks = []
        self.userBookstr = ""
        for book in AllBooks:
            if book[5] == userID:
                self.userBookstr += f"{book[0]}\nРяд: {book[1] + 1}\nМесто: {book[2] + 1}\nФильм: {book[3]}\nНачало: {book[4]}\n"
                self.userBooks.append(book[0])
        if len(self.userBooks) == 0:
            self.bot.send_message(chat_id=self.id, text="Пока что нет действительных броней")
            return (SI_START, True)
        else:
            self.bot.send_message(chat_id=self.id, text=self.userBookstr)
            delBookKeyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            for book in self.userBooks:
                delBookKeyboard.add(telebot.types.KeyboardButton(text=book))
            self.bot.send_message(
                chat_id=self.id,
                text="Выбирите бронь которую хотите отменить",
                reply_markup=delBookKeyboard,
            )
            return SI_DELBOOKSTEPTWO
        
    def state_del_book_step_two(self, message: telebot.types.Message, stateid):
        delbook = message.text
        if not (delbook in self.userBooks):
            self.bot.send_message(chat_id=self.id, text="Данная бронь уже неактивна")
            return (SI_DELBOOK, True)
        else:
            sql3Funcs.delete_from_table("tiket.db", "books", "uuid", delbook)
            self.bot.send_message(chat_id=self.id, text="Бронь удалена")
            return (SI_START, True)
        
    def state_order(self, message: telebot.types.Message, stateid):
        keyboard5 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        keyboard5.add(
            telebot.types.KeyboardButton(text="Получить помощь"),
            telebot.types.KeyboardButton(text="Главное меню"),
        )
        self.bot.send_message(
            chat_id=self.id,
            text="Получить помощь системы в подборе фильма🔧\nГлавное меню",
            reply_markup=keyboard5,
        )
        return SI_ORDER_MENU

    def state_order_menu(self, message: telebot.types.Message, stateid):
        if message.text == "Получить помощь":
            return (SI_BOOK_WITH_HELP, True)
        if message.text == "Главное меню":
            return (SI_BOOK_MANUAL, True)
        return (SI_START, True)

    def state_book_with_help(self, message: telebot.types.Message, stateid):
        films, _ = self._cinema.get_films()
        keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in films:
            keyboard.add(telebot.types.KeyboardButton(text=str(i)))
        self.bot.send_message(
            chat_id=self.id,
            text="Выберите интересующий вас фильм🎥:",
            reply_markup=keyboard,
        )
        self.bot.send_sticker(
            self.id,
            "CAACAgUAAxkBAAEM5S5m-QewK3A8rLoaaALi5EGqp-DTdgACBgkAAuG4GVTEA6nSvXlrXDYE",
        )
        return SI_CHOOSE_FILM

    def state_book_manual(self, message: telebot.types.Message, stateid):
        # TODO: Доделать
        return (SI_START, True)

    def state_choose_film(self, message: telebot.types.Message, stateid):
        films, _ = self._cinema.get_films()
        self.film = message.text
        if message.text in films:
            return (SI_CHOOSE_HALL, True)
        self.bot.send_message(
            chat_id=message.chat.id, text="Такой фильм сегодня не показывают😞"
        )
        return (SI_BOOK_WITH_HELP, True)

    def state_choose_hall(self, message: telebot.types.Message, stateid):
        halls, info = self._cinema.get_halls(self.film)
        self.bot.send_message(chat_id=self.id, text=info)
        keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)

        for i in halls:
            keyboard2.add(telebot.types.KeyboardButton(text=str(i)))
        self.bot.send_message(
            chat_id=self.id, text="Выбирите зал🎥: ", reply_markup=keyboard2
        )
        return SI_CHOOSE_HALL_DONE

    def state_choose_hall_done(self, message: telebot.types.Message, stateid):
        halls, _ = self._cinema.get_halls(self.film)
        self.hall = message.text
        if self.hall in halls:
            return (SI_CHOOSE_TIME, True)
        self.bot.send_message(
            chat_id=message.chat.id, text="Такого зала не существует😞"
        )
        return (SI_CHOOSE_HALL, True)

    def state_choose_time(self, message: telebot.types.Message, stateid):
        times, info = self._cinema.get_times(self.film, self.hall)
        self.bot.send_message(chat_id=self.id, text=info)
        keyboard3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        for i in times:
            keyboard3.add(telebot.types.KeyboardButton(text=str(i)))
        self.bot.send_message(
            chat_id=message.chat.id, text="Выбирите время⏰: ", reply_markup=keyboard3
        )
        return SI_CHOOSE_TIME_DONE

    def state_choose_time_done(self, message: telebot.types.Message, stateid):
        self.time = message.text
        times, _ = self._cinema.get_times(self.film, self.hall)
        if self.time in times:
            return (SI_CHOOSE_TIME_OK, True)
        self.bot.send_message(
            chat_id=message.chat.id, text="В это время нет киносеансов😞"
        )
        return (SI_CHOOSE_TIME, True)

    def state_choose_time_ok(self, message: telebot.types.Message, stateid):
        self.bot.send_message(chat_id=message.chat.id, text="Готово")
        return (SI_CHOOSE_PLACE, True)
    
    
    def state_see_sites(self, message: telebot.types.Message, stateid):
        self.bookedSeates = sql3Funcs.get_from_table("tiket.db", "books")
        for i in range(len(self._cinema.halls)):
            if self.hall == self._cinema.halls[i].name:
                self.chooseHall = self._cinema.halls[i]
        mainstring = len(str(self.chooseHall.column)) * " " + "  "

        for i in range(self.chooseHall.row):
            if i == 0:
                mainstring += "1"

            else:
                mainstring += ((len(str(self.chooseHall.row)) - len(str(i))) * " " + "  ") + str((i + 1))
        mainstring += "\n"

        for i in range(self.chooseHall.column):
            for j in range(self.chooseHall.row):

                if chek((i, j, self.film, self.time), self.bookedSeates):

                    if j == 0:
                        mainstring += str(i + 1) + ((len(str(self.chooseHall.column)) - len(str(i + 1))) * " " + " |")
                    mainstring += "*" + (len(str(self.chooseHall.row)) * " " + " ")

                else:
                    if j == 0:
                        mainstring += str(i + 1) + ((len(str(self.chooseHall.column)) - len(str(i + 1))) * " " + " |")
                    mainstring += "o" + (len(str(self.chooseHall.row)) * " " + " ")
            mainstring += "\n"
        mainstring += "* - место знято😞\n"
        mainstring += "o - место свободно😄\n"
        self.bot.send_message(chat_id=message.chat.id, text=mainstring)

        self.bot.send_message(chat_id=message.chat.id, text="Введите ряд🪑: ")
        return SI_CONTUNIE_CHOOSE
    
    def state_contunie_choose_place(self, message: telebot.types.Message, stateid):
        try:
            self.row = int(message.text)
        except ValueError:
            self.bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так😵‍💫")
            return (SI_CHOOSE_PLACE, True)
        self.bot.send_message(chat_id=message.chat.id, text="Введите место🪑: ")
        return SI_CONTUNIE_SIET

    def state_contunie_choose_site(self, message: telebot.types.Message, stateid):
        self.bookedSeates = sql3Funcs.get_from_table("tiket.db", "books")
        try:
            self.seat = int(message.text)
        except ValueError:
            self.bot.send_message(chat_id=message.chat.id, text="Что-то пошло не так😵‍💫")
            return (SI_CHOOSE_PLACE, True)
        if chek((self.seat - 1, self.row - 1, self.film, self.time), self.bookedSeates):
            self.bot.send_message(chat_id=message.chat.id, text="Это место уже занято или его не сушествует")
            return (SI_CHOOSE_PLACE, True)
        if self.row > self.chooseHall.column:
            self.bot.send_message(chat_id=message.chat.id, text="Это место уже занято или его не сушествует")
            return (SI_CHOOSE_PLACE, True)
        if  self.seat > self.chooseHall.row:
            self.bot.send_message(chat_id=message.chat.id, text="Это место уже занято или его не сушествует")
            return (SI_CHOOSE_PLACE, True)
        if  self.row <= 0 or self.seat <= 0:
            self.bot.send_message(chat_id=message.chat.id, text="Это место уже занято или его не сушествует")
            return (SI_CHOOSE_PLACE, True)
        self.uid = uuid.uuid4()
        sql3Funcs.insert_into_table("tiket.db", "books", uuid=self.uid, row=self.row-1, sits=self.seat-1, move=self.film, time=self.time, id=self.user.id)
        self.bot.send_message(chat_id=message.chat.id, text=f"Номер вашего заказа: {self.uid}")
        return (SI_START, True)