import asyncio
import os
import logging
from handlers import dp

from aiogram import Bot
from dotenv import load_dotenv

async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=os.environ["TOKEN"])

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())