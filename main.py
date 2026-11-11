import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher

from handlers.commands.basic_handlers import basic_router
from handlers.commands.create_monitor import create_monitor_form_router
from handlers.commands.monitors import monitor_router


async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO)

    dp = Dispatcher()
    dp.include_routers(basic_router, create_monitor_form_router, monitor_router)

    bot = Bot(token=os.environ["TOKEN"])

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.send_message(chat_id=os.environ["DEV_CHAT_ID"],text="Bot is started.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())