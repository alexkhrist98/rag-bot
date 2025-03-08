import asyncio
import os
import logging

from backend.index_builder import IndexBuilder
from bot.bot import Bot

def main() -> None:
    DEBUG = os.getenv("DEBUG")
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    logging.info("Start building index")
    BUILD_INDEX = os.getenv("BUILD_INDEX", None)
    if bool(BUILD_INDEX):
        IndexBuilder().build_index()
    logging.info("Index complete")
    logging.info("Starting bot")
    bot:Bot = Bot(API_TOKEN)
    asyncio.run(bot.start())

if __name__ == "__main__":
    main()