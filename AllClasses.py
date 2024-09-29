import telebot

class Movies:
    def __init__(self, name, duringInMinutes) -> None:
        self.name = name
        self.during = duringInMinutes

    def __str__(self) -> str:
        return f"Название: {self.name}\nПродолжительность: {self.during} минут(ы)"


def createFilm(message, bot) -> Movies:
    bot.send_message(chat_id=message.chat.id, text="Введите название фильма: ")
    name = message.text
    bot.send_message(chat_id=message.chat.id, text="Введите продолжительность фильма: ")
    during = int(message.text)
    return Movies(name, during)


class CinemaHall:
    bookedSeates = []

    def __init__(self, row, column, name, moviesAndTime) -> None:
        self.row = row
        self.column = column
        self.name = name
        self.moviesAndTime = moviesAndTime

    def __str__(self) -> str:
        string = f"Кинозал: {self.name}\nКолличество мест: {self.row * self.column}\n\nКиносиансы:\n"
        for key, value in self.moviesAndTime.items():
            minutes = int(key.split(":")[1])
            minutes = minutes + value.during % 60
            if len(str(minutes)) == 1:
                minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
            houers = int(key.split(":")[0])
            string = string + f"{value.name} - Начало: {key} - Конец: {houers + value.during // 60}:{minutes}\n({str(value)})\n"
        return string[0:len(string) - 1]

    def book(self, message, bot, time=None, move=None) -> None:
        if time == None and move == None:
            moves = []
            times = []
            string = ""
            for key, value in self.moviesAndTime.items():
                moves.append(value.name)
                times.append(key)
                minutes = int(key.split(":")[1])
                minutes = minutes + value.during % 60
                if len(str(minutes)) == 1:
                    minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
                houers = int(key.split(":")[0])
                string = string + f"{value.name} - Начало: {key} - Конец: {houers + value.during // 60}:{minutes}\n({str(value)})\n"
            bot.send_message(chat_id=message.chat.id, text=string[0:len(string) - 1])
            d = []
            for i in move:
                d.append(telebot.types.KeyboardButton(text=str(i)))
            moveKeybord = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            moveKeybord.add(*d)
            bot.send_message(chat_id=message.chat.id, text="Введите название фильма: ", reply_markup=moveKeybord)
            move = message.text
            while not (move in moves):
                bot.send_message(chat_id=message.chat.id, text="Сегодня такой фильм не показывают. Введите название фильма: ", reply_markup=moveKeybord)
                move = message.text
            d = []
            for i in time:
                d.append(telebot.types.KeyboardButton(text=str(i)))
            moveKeybord = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            moveKeybord.add(*d)
            bot.send_message(chat_id=message.chat.id, text="Выбирете время: ", reply_markup=moveKeybord)
            time = message.text
            while not (time in times):
                bot.send_message(chat_id=message.chat.id, text="Сегодня в это время фильм не показывают. Выбирете время: ", reply_markup=moveKeybord)
                time = message.text
        mainstring = len(str(self.column)) * " " + "  "
        for i in range(self.row):
            if i == 0:
                mainstring += str(i + 1)
            else:
                mainstring += str(((len(str(self.row)) - len(str(i))) * " " + "  ") + str((i + 1)))
                mainstring += "\n"
        for i in range(self.column):
            for j in range(self.row):
                if (move, i, j, time) in self.bookedSeates:
                    if j == 0:
                        mainstring += str(str(i + 1) + ((len(str(self.column)) - len(str(i + 1))) * " " + " |"))
                    mainstring += str("*" + (len(str(self.row)) * " " + " "))
                else:
                    if j == 0:
                        mainstring += str(str(i + 1) + ((len(str(self.column)) - len(str(i + 1))) * " " + " |"))
                    mainstring += str("o", + (len(str(self.row)) * " " + " "))
            mainstring += "\n"
        mainstring += "* - место знято\n"
        mainstring += "o - место свободно\n"
        qwKeyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        qwKeyboard.add(
            telebot.types.KeyboardButton(text='Да'),
            telebot.types.KeyboardButton(text='Нет')
        )
        bot.send_message(chat_id=message.chat.id, text=mainstring)
        bot.send_message(chat_id=message.chat.id, text="Продолжить выбор места?", reply_markup=qwKeyboard)
        target = message.text
        if target != "Да":
            return
        bot.send_message(chat_id=message.chat.id, text="Введите ряд: ")
        row = int(message.text)
        bot.send_message(chat_id=message.chat.id, text="Введите место: ")
        seat = int(message.text)
        while row > self.column or seat > self.row or row <= 0 or seat <= 0 or (
        move, seat, row, time) in self.bookedSeates:
            bot.send_message(chat_id=message.chat.id, text="Это место уже занято или его не сушествует")
            bot.send_message(chat_id=message.chat.id, text="Введите ряд: ")
            row = int(message.text)
            bot.send_message(chat_id=message.chat.id, text="Введите место: ")
            seat = int(message.text)
        self.bookedSeates.append((move, row - 1, seat - 1, time))

    def cancelAllBooks(self) -> None:
        self.bookedSeates.clear()
        print("Все брони отменены")

    def append(self, message, bot) -> None:
        namberKeybord = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        namberKeybord.add(
            telebot.types.KeyboardButton(text='1'),
            telebot.types.KeyboardButton(text='2'),
            telebot.types.KeyboardButton(text='3'),
            telebot.types.KeyboardButton(text='4'),
            telebot.types.KeyboardButton(text='5'),
            telebot.types.KeyboardButton(text='6'),
            telebot.types.KeyboardButton(text='7'),
            telebot.types.KeyboardButton(text='8'),
            telebot.types.KeyboardButton(text='9')
        )
        bot.send_message(chat_id=message.chat.id, text="Введите какое количество фильмов вы желаете добавить: ",
                         reply_markup=namberKeybord)
        for i in range(int(message.text)):
            bot.send_message(chat_id=message.chat.id, text="Введите начало фильма: ",
                         reply_markup=namberKeybord)
            time = message.text
            self.moviesAndTime[time] = createFilm(message, bot)


def createHall(bot, message) -> CinemaHall:
    namberKeybord = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    namberKeybord.add(
        telebot.types.KeyboardButton(text='1'),
        telebot.types.KeyboardButton(text='2'),
        telebot.types.KeyboardButton(text='3'),
        telebot.types.KeyboardButton(text='4'),
        telebot.types.KeyboardButton(text='5'),
        telebot.types.KeyboardButton(text='6'),
        telebot.types.KeyboardButton(text='7'),
        telebot.types.KeyboardButton(text='8'),
        telebot.types.KeyboardButton(text='9'),
        telebot.types.KeyboardButton(text='10'),
        telebot.types.KeyboardButton(text='11'),
        telebot.types.KeyboardButton(text='12'),
        telebot.types.KeyboardButton(text='13'),
        telebot.types.KeyboardButton(text='14'),
        telebot.types.KeyboardButton(text='16')
    )
    bot.send_message(chat_id=message.chat.id, text="Введите количество кресел в ряду: ",
                         reply_markup=namberKeybord)
    row = int(message.text)
    bot.send_message(chat_id=message.chat.id, text="Введите количество рядов: ",
                         reply_markup=namberKeybord)
    column = int(message.text)
    bot.send_message(chat_id=message.chat.id, text="Введите название зала: ",
                         reply_markup=namberKeybord)
    name = message.text
    return CinemaHall(row, column, name, dict())


class Cinema:
    def __init__(self, name, halls) -> None:
        self.name = name
        self.halls = halls

    def __str__(self) -> str:
        j = 1
        string = f"Кинотеатр: {self.name}\nКинозалы:\n\n"
        for i in self.halls:
            string = string + str(j) + ":" + "\n" + str(i) + "\n"
            j += 1
        return string[0:len(string) - 1]

    def append(self, message, bot) -> None:
        namberKeybord = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        namberKeybord.add(
            telebot.types.KeyboardButton(text='1'),
            telebot.types.KeyboardButton(text='2'),
            telebot.types.KeyboardButton(text='3'),
            telebot.types.KeyboardButton(text='4'),
            telebot.types.KeyboardButton(text='5'),
            telebot.types.KeyboardButton(text='6'),
            telebot.types.KeyboardButton(text='7'),
            telebot.types.KeyboardButton(text='8'),
            telebot.types.KeyboardButton(text='9')
        )
        bot.send_message(chat_id=message.chat.id, text="Введите сколько заллов хотите создать: ",
                         reply_markup=namberKeybord)
        for i in range(int(message.text)):
            d = createHall(bot, message)
            d.append(message, bot)
            self.halls.append(d)

    # def book(self) -> None:
    #     halls = []
    #     print("Кинозалы:")
    #     for i in self.halls:
    #         print(i.name)
    #         halls.append(i.name)
    #     hall = input("Введите название зала: ")
    #     while not (hall in halls):
    #         print("Такого кинозала не сушествует")
    #         hall = input("Введите название зала: ")
    #     self.halls[halls.index(hall)].book()
    def book(self, bot, message, menuKeyboard) -> None:
        bot.send_message(chat_id=message.chat.id, text='Получить помощь системы в подборе фильма\nВыбрать фильм самостоятельно',
                         reply_markup=menuKeyboard)
        target = message.text()
        if target == "Да":
            b = []
            films = set()

            for i in self.halls:
                for key, value in i.moviesAndTime.items():
                    b.append((i, value, key))
                    films.add(value.name)
            d = []
            for i in films:
                d.append(telebot.types.KeyboardButton(text=str(i)))

            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.add(*d)
            bot.send_message(chat_id=message.chat.id, text='Выбирите интересующий вас фильм:',
                         reply_markup=keyboard)
            target1 = message.text
            while not (target1 in films):
                bot.send_message(chat_id=message.chat.id, text='Такой фильм сегодня не показывают. Выбирите интересующий вас фильм:',
                                 reply_markup=keyboard)
                target1 = message.text
            halls = set()
            string1 = ""
            for i in b:
                if i[1].name == target1:
                    halls.add(i[0].name)
                    minutes = int(i[2].split(":")[1])
                    houers = int(i[2].split(":")[0])
                    minutes = minutes + value.during % 60
                    if len(str(minutes)) == 1:
                        minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
                    string1 += (
                        f"Кинотеатр: {self.name}\nЗал: {i[0].name}\nВремя:{i[2]}-{houers + i[1].during // 60}:{minutes}\n")
            bot.send_message(chat_id=message.chat.id, text=string1)
            d = []
            for i in halls:
                d.append(telebot.types.KeyboardButton(text=str(i)))
            keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard2.add(*d)
            bot.send_message(chat_id=message.chat.id, text="Выбирите зал: ", reply_markup=keyboard2)
            target3 = message.text
            while not (target3 in halls):
                bot.send_message(chat_id=message.chat.id, text="Такого зала не существует. Выбирите зал: ", reply_markup=keyboard2)
                target3 = message.text
            time = set()
            string2 = ""
            for i in b:
                if i[1].name == target1 and i[0].name == target3:
                    time.add(i[2])
                    minutes = int(i[2].split(":")[1])
                    if len(str(minutes)) == 1:
                        minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
                    houers = int(i[2].split(":")[0])
                    string2 += (
                        f"Кинотеатр: {self.name}\nЗал: {i[0].name}\nВремя:{i[2]}-{houers + i[2].during // 60}:{minutes}")
            bot.send_message(chat_id=message.chat.id, text=string2)
            d = []
            for i in time:
                d.append(telebot.types.KeyboardButton(text=str(i)))
            keyboard3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard3.add(*d)
            bot.send_message(chat_id=message.chat.id, text="Выбирите время: ", reply_markup=keyboard3)
            target4 = message.text
            while not (target4 in time):
                bot.send_message(chat_id=message.chat.id, text="В это время нет киносеансов. Выбирите время: ", reply_markup=keyboard3)
                target4 = message.text
            string3 = ""
            for i in b:
                if i[1].name == target1 and i[0].name == target3 and i[2] == target4:
                    minutes = int(i[2].split(":")[1])
                    if len(str(minutes)) == 1:
                        minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
                    houers = int(i[2].split(":")[0])
                    string3 += (
                        f"Кинотеатр: {i[0].name}\nЗал: {i[1].name}\nВремя:{i[3]}-{houers + i[2].during // 60}:{minutes}")
                    i[1].book(i[3], i[2].name)
                    bot.send_message(chat_id=message.chat.id, text=string3)



        else:
            halss = []
            for i in self.halls:
                halss.append(i.name)
            d = []
            for i in halls:
                d.append(telebot.types.KeyboardButton(text=str(i)))
            keyboard4 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard4.add(*d)
            bot.send_message(chat_id=message.chat.id, text="Введите название кинозала: ", reply_markup=keyboard4)
            hall = message.text
            while not (hall in halls):
                bot.send_message(chat_id=message.chat.id, text="Такого кинотеатра не сушествует. Введите название кинозала: ", reply_markup=keyboard4)
                halss = message.text
            self.halls[halls.index(hall)].book()

# def createCinema() -> Cinema:
#     return Cinema(input("Введите название кинотеатра: "), [])
#
#
# class SystemOfCinema:
#     def __init__(self, cinemas, name) -> None:
#         self.cinemas = cinemas
#         self.name = name
#
#     def __str__(self) -> str:
#         string = f"Название компании: {self.name}\nКинотеатры:\n"
#         j = 1
#         for i in self.cinemas:
#             string = string + str(j) + ":" + "\n" + str(i) + "\n"
#             j += 1
#         return string[0:len(string) - 1]
#
#     def append(self) -> None:
#         s = createCinema()
#         s.append()
#         self.cinemas.append(s)
#
#     def book(self) -> None:
#         target = input(
#             "Получить помощь системы в подборе кинотеатра(1)\nВыбрать кинотеатр самостоятельно(любой другой сивол)\n")
#         if target == "1":
#             b = []
#             cinemas_names = set()
#             films = set()
#             for i in self.cinemas:
#                 for j in range(len(i.halls)):
#                     for key, value in i.halls[j].moviesAndTime.items():
#                         b.append((i, i.halls[j], value, key))
#                         films.add(value.name)
#                         cinemas_names.add(i.name)
#             # target = input("Берёте билеты для группы(1) Для себя(любой другой символ) ")
#             # if target == "1":
#             #     while True:
#             #         try:
#             #             groop = int(input("Введите размер вашей группы: "))
#             #         except ValueError:
#             #             print("Ошибка")
#             #         else:
#             #             break
#             #     cin = input("Введите название кинотеатра: ")
#             #     while not (cin in cinemas_names):
#             #         print("Такого кинотеатра не существует")
#             #         cin = input("Введите название кинотеатра: ")
#             #     for i in self.cinemas:
#             #         if cin == i.name:
#             #             cinem = i
#             #     for i in cinem.halls:
#             #         pass
#             #         # for j in range(len(i.halls)):
#             #         #     l = []
#             #         #     for key, value in i.halls[j].moviesAndTime.items():
#             #         #         l.append(key)
#             #         #     for k in i.halls[j].bookedSeates.copy():
#             #         #         h = []
#             #         #         for o in l:
#             #         #             if k[3] == o:
#             #         #                 for e in range(i.halls[j].column):
#             #         #                     if k[1] == e:
#             #         #                         h.append(k)
#
#             # else:
#             print("Фильмы:")
#             for i in films:
#                 print(i)
#             target1 = input("Выбирите интересующий вас фильм: ")
#             while not (target1 in films):
#                 print("Такой фильм сегодня не показывают")
#                 target1 = input("Выбирите интересующий вас фильм: ")
#             cinemas2 = set()
#             for i in b:
#                 if i[2].name == target1:
#                     cinemas2.add(i[0].name)
#                     minutes = int(i[3].split(":")[1])
#                     minutes = minutes + value.during % 60
#                     if len(str(minutes)) == 1:
#                         minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
#                     houers = int(i[3].split(":")[0])
#                     print(
#                         f"Кинотеатр: {i[0].name}\nЗал: {i[1].name}\nВремя:{i[3]}-{houers + i[2].during // 60}:{minutes}")
#             target2 = input("Выбирите кинотеатр: ")
#             while not (target2 in cinemas2):
#                 print("Такого кинотеатра не существует")
#                 target2 = input("Выбирите кинотеатр: ")
#             halls = set()
#             for i in b:
#                 if i[0].name == target2 and i[2].name == target1:
#                     halls.add(i[1].name)
#                     minutes = int(i[3].split(":")[1])
#                     houers = int(i[3].split(":")[0])
#                     minutes = minutes + value.during % 60
#                     if len(str(minutes)) == 1:
#                         minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
#                     print(
#                         f"Кинотеатр: {i[0].name}\nЗал: {i[1].name}\nВремя:{i[3]}-{houers + i[2].during // 60}:{minutes}")
#             target3 = input("Выбирите зал: ")
#             while not (target3 in halls):
#                 print("Такого зала не существует")
#                 target3 = input("Выбирите зал: ")
#             time = set()
#             for i in b:
#                 if i[0].name == target2 and i[2].name == target1 and i[1].name == target3:
#                     time.add(i[3])
#                     minutes = int(i[3].split(":")[1])
#                     if len(str(minutes)) == 1:
#                         minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
#                     houers = int(i[3].split(":")[0])
#                     print(
#                         f"Кинотеатр: {i[0].name}\nЗал: {i[1].name}\nВремя:{i[3]}-{houers + i[2].during // 60}:{minutes}")
#             target4 = input("Выбирите время: ")
#             while not (target4 in time):
#                 print("В это время нет киносеансов")
#                 target4 = input("Выбирите время: ")
#             for i in b:
#                 if i[0].name == target2 and i[2].name == target1 and i[1].name == target3 and i[3] == target4:
#                     minutes = int(i[3].split(":")[1])
#                     if len(str(minutes)) == 1:
#                         minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
#                     houers = int(i[3].split(":")[0])
#                     print(
#                         f"Кинотеатр: {i[0].name}\nЗал: {i[1].name}\nВремя:{i[3]}-{houers + i[2].during // 60}:{minutes}")
#                     i[1].book(i[3], i[2].name)
#
#
#
#         else:
#             cinemas = []
#             print("Кинозалы:")
#             for i in self.cinemas:
#                 print(i.name)
#                 cinemas.append(i.name)
#             cinema = input("Введите название кинотеатра: ")
#             while not (cinema in cinemas):
#                 print("Такого кинотеатра не сушествует")
#                 cinema = input("Введите название кинотеатра: ")
#             self.cinemas[cinemas.index(cinema)].book()

