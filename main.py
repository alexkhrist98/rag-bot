import asyncio
import os
import logging

from backend.index_builder import IndexBuilder
from bot.bot import Bot

def main() -> None:
    LOG_LEVEL = int(os.getenv("LOG_LEVEL", '0'))
    logging.basicConfig(level=LOG_LEVEL)
    API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    logging.info("Start building index")
    IndexBuilder().build_index()
    logging.info("Index complete")
    logging.info("Starting bot")
    bot:Bot = Bot(API_TOKEN)
    asyncio.run(bot.start())

if __name__ == "__main__":
    main()