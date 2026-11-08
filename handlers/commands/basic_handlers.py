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


@basic_router.message(Command("monitor"))
async def monitor_command(message: Message):
    # await message.answer("Type the URL below:")
    # await message.answer(message.text)

    parts = (message.text or "").split(maxsplit=1)

    if len(parts) < 2:
        await message.reply("Choose the adress: /monitor https://example.com")
        return

    html_page = await parser.parse(parts[1])

    if html_page is None:
        await message.reply("Can't load page. Check the address.")
    else:
        await message.answer_document(html_page)

# @basic_router.message()
# async def echo (message: Message):
#     # await message.reply("I don't know how to handle that yet. Try /help.")
#     await message.react([ReactionTypeEmoji(emoji="🔥", type='emoji')], True)
