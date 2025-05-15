import asyncio

from app.config import settings
from app.bot.bot import ber_bot
from app.database import Base, engine

async def start_base():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.run(start_base())
    ber_bot(settings.BOT_TOKEN)
