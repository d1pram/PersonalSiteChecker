from aiogram import Dispatcher, Router, F, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, ReactionTypeEmoji, MessageReactionUpdated
import parser


basic_router = Router()

@basic_router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hi! I'm Site Checker. Use /help to see what I can do.", reply_markup=ReplyKeyboardRemove())


@basic_router.message(Command("help"))
async def help_command(message: Message):
    await message.answer("/start — welcome message\n/help — show available commands")

# @basic_router.message()
# async def echo (message: Message):
#     # await message.reply("I don't know how to handle that yet. Try /help.")
#     await message.react([ReactionTypeEmoji(emoji="🔥", type='emoji')], True)
