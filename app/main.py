from app.config import settings
from app.bot import berber_bot

if __name__ == '__main__':
    berber_bot(settings.BOT_TOKEN)
