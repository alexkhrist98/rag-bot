import asyncio
import os
import logging

from bot.bot import Bot

def main() -> None:
    API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    bot:Bot = Bot(API_TOKEN)
    asyncio.run(bot.start())

if __name__ == "__main__":
    main()