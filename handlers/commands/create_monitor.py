import asyncio
import json
import logging
from uuid import uuid4

import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery


from keybords import create_url_state_keyboard

create_monitor_form_router = Router()

class MonitorStates(StatesGroup):
    name = State()
    url = State()
    purpose = State()


@create_monitor_form_router.message(Command("create_monitor"))
async def create_monitor_command(message: Message, state: FSMContext) :
    await state.set_state(MonitorStates.name)
    await message.answer(
        "Hi there! So how should this monitor be called?",
        reply_markup=ReplyKeyboardRemove(),
    )

@create_monitor_form_router.message(MonitorStates.name, F.text)
async def process_name(message: Message, state: FSMContext) :
    await state.update_data(name=message.text)
    await state.set_state(MonitorStates.url)
    await message.reply("Okay good, now you can type your URL:\n|| Include http:// or https:// ||", parse_mode="MarkdownV2")


@create_monitor_form_router.message(MonitorStates.url, F.text)
async def process_url(message: Message, state: FSMContext):
    url = message.text.strip()

    if not url.startswith(("http://", "https://")):
        await message.reply("Invalid URL. Try again with https:// or http://")
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(message.text) as response:
                response.raise_for_status()
    except (aiohttp.ClientConnectionError, asyncio.TimeoutError, aiohttp.client_exceptions) as err:
        logging.error(err)
        await message.reply("Something went wrong :( Try again.")
        return


    await state.update_data(url=url)
    await state.set_state(MonitorStates.purpose)
    await message.answer("The URL is good, now tell me what you want to track", reply_markup=create_url_state_keyboard(url))


def save_monitor(name, url, purpose, user_id):
    user_id = str(user_id)

    monitor = {
        "id": uuid4().hex,
        "name": name,
        "url": url,
        "purpose": purpose,
    }

    try:
        with open("monitors.json", "r", encoding="utf-8") as file:
            storage = json.load(file)
    except FileNotFoundError:
        storage = {}

    storage.setdefault(user_id, {"monitors": []})
    storage[user_id]["monitors"].append(monitor)

    with open("monitors.json", "w", encoding="utf-8") as file:
        json.dump(storage, file, ensure_ascii=False, indent=2)

@create_monitor_form_router.callback_query(MonitorStates.purpose)
async def page_changes(query: CallbackQuery, state: FSMContext):
    await state.update_data(purpose=query.data)

    if query.data == "number_check":
        await query.answer(show_alert=True, text="Number check mode is set.\nTo see more details do «/help Number check»")
    elif query.data == "page_changes":
        await query.answer(show_alert=True, text="Changes in page mode is set.\nTo see more details do «/help Changes in page»")


    await query.message.edit_text(f"Changes in page mode is set to {query.data}\n"
                                  f"Now your monitor is ready to go! Check your monitors on /monitors")


    # Should create a Monitor object and store it somehow
    # The idea is to store it as JSON, giving each user it's monitors
    data = await state.get_data()
    save_monitor(data['name'],data['url'], data['purpose'], user_id=query.from_user.id)
    await state.clear()