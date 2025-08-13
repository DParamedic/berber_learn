from app.bot import berber_bot
from app.config import settings

if __name__ == '__main__':
    berber_bot(settings.TELEGRAM_BOT_TOKEN)