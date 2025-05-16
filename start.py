from app.bot.bot import ber_bot
from app.config import settings

if __name__ == '__main__':
    ber_bot(settings.TELEGRAM_BOT_TOKEN)