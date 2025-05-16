from app.config import settings
from app.bot.bot import ber_bot

if __name__ == '__main__':
    ber_bot(settings.BOT_TOKEN)
