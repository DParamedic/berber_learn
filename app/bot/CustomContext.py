from telegram.ext import ContextTypes

from app.bot.UserData import UserData

class CustomContext(ContextTypes.DEFAULT_TYPE):
    def __init__(self, application, chat_id = None, user_id = None):
        super().__init__(application, chat_id, user_id)

    @property
    def user_data_(self):
        if not "data" in self.user_data:
            self.user_data["data"] = UserData()
        return self.user_data["data"]

    @property
    def chat_id(self):
        return self._chat_id
