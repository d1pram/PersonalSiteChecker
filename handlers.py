from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Hi! I'm Site Checker. Use /help to see what I can do.")


@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("/start — welcome message\n/help — show available commands")


@dp.message()
async def fallback(message: Message):
    await message.answer("I don't know how to handle that yet. Try /help.")
