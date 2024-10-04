import sql3Funcs
from stateMachine import StateMachine
import telebot


class Session:
    def __init__(self, user, chatid, bot: telebot.TeleBot):
        self.user = user
        self.id = chatid
        self.bot = bot
        self.state_machine = StateMachine()

    def onMessage(self, message: telebot.types.Message):
        if not self.state_machine.handleState(message):
            self.state_machine.reset()
            self.state_machine.handleState(message)

