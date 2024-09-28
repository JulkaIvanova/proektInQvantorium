import telebot
bot1 = telebot.TeleBot('6338167935:AAHo7RLEwHykLY0_EnBiMVuN4tN1tIu6EzQ')

class Movies:
    def __init__(self, name, duringInMinutes) -> None:
        self.name = name
        self.during = duringInMinutes

    def __str__(self) -> str:
        return f"Название: {self.name}\nПродолжительность: {self.during} минут(ы)"


def createFilm() -> Movies:
    return Movies(input("Введите название фильма: "), int(input("Введите продолжительность фильма: ")))


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

    def book(self, time=None, move=None) -> None:
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
            print(string[0:len(string) - 1])
            move = input("Введите название фильма: ")
            while not (move in moves):
                print("Сегодня такой фильм не показывают")
                move = input("Введите название фильма: ")
            time = input("Выбирете время: ")
            while not (time in times):
                print("Сегодня в это время фильм не показывают")
                time = input("Выбирете время: ")
        print(len(str(self.column)) * " " + "  ", end="")
        for i in range(self.row):
            if i == 0:
                print(i + 1, end="")
            else:
                print(((len(str(self.row)) - len(str(i))) * " " + "  ") + str((i + 1)), end="")
        print("")
        for i in range(self.column):
            for j in range(self.row):
                if (move, i, j, time) in self.bookedSeates:
                    if j == 0:
                        print(i + 1, end=(len(str(self.column)) - len(str(i + 1))) * " " + " |")
                    print("*", end=len(str(self.row)) * " " + " ")
                else:
                    if j == 0:
                        print(i + 1, end=(len(str(self.column)) - len(str(i + 1))) * " " + " |")
                    print("o", end=len(str(self.row)) * " " + " ")
            print("\n", end="")
        print("* - место знято")
        print("o - место свободно")
        target = input("Продолжить выбор места? Да(1) Нет(любой другой символ) ")
        if target != "1":
            return
        row = int(input("Введите ряд: "))
        seat = int(input("Введите место: "))
        while row > self.column or seat > self.row or row <= 0 or seat <= 0 or (
        move, seat, row, time) in self.bookedSeates:
            print("Это место уже занято или его не сушествует")
            row = int(input("Введите ряд: "))
            seat = int(input("Введите место: "))
        self.bookedSeates.append((move, row - 1, seat - 1, time))

    def cancelAllBooks(self) -> None:
        self.bookedSeates.clear()
        print("Все брони отменены")

    def append(self) -> None:
        for i in range(int(input("Введите какое количество фильмов вы желаете добавить: "))):
            self.moviesAndTime[input("Введите начало фильма: ")] = createFilm()


def createHall() -> CinemaHall:
    return CinemaHall(int(input("Введите количество кресел в ряду: ")), int(input("Введите количество рядов: ")),
                      input("Введите название зала: "), dict())


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

    def append(self) -> None:
        for i in range(int(input("Введите сколько заллов хотите создать: "))):
            d = createHall()
            d.append()
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
        bot = bot1
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
            w = []
            for i in films:
                w.append(i)

            keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard.add(*w)
            bot.send_message(chat_id=message.chat.id, text='Выбирите интересующий вас фильм:',
                         reply_markup=keyboard)
            target1 = message.text
            while not (target1 in films):
                bot.send_message(chat_id=message.chat.id, text='Такой фильм сегодня не показывают. Выбирите интересующий вас фильм:',
                                 reply_markup=keyboard)
                target2 = message.text
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
            keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            keyboard2.add(*halls)
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
            target4 = input("Выбирите время: ")
            while not (target4 in time):
                print("В это время нет киносеансов")
                target4 = input("Выбирите время: ")
            for i in b:
                if i[0].name == target2 and i[2].name == target1 and i[1].name == target3 and i[3] == target4:
                    minutes = int(i[3].split(":")[1])
                    if len(str(minutes)) == 1:
                        minutes = str(minutes).replace(str(minutes), "0" + str(minutes))
                    houers = int(i[3].split(":")[0])
                    print(
                        f"Кинотеатр: {i[0].name}\nЗал: {i[1].name}\nВремя:{i[3]}-{houers + i[2].during // 60}:{minutes}")
                    i[1].book(i[3], i[2].name)



        else:
            cinemas = []
            print("Кинозалы:")
            for i in self.cinemas:
                print(i.name)
                cinemas.append(i.name)
            cinema = input("Введите название кинотеатра: ")
            while not (cinema in cinemas):
                print("Такого кинотеатра не сушествует")
                cinema = input("Введите название кинотеатра: ")
            self.cinemas[cinemas.index(cinema)].book()

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

