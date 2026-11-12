import asyncio
import json
import logging
from uuid import uuid4
import ssl
import certifi
import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from handlers.states import MonitorStates
from keybords import(
    create_url_state_keyboard,
    create_monitor_approval_keyboard,
)

create_monitor_form_router = Router()

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
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context)

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                response.raise_for_status()

    except (aiohttp.ClientError, asyncio.TimeoutError) as err:
        logging.error(err)
        await message.reply("Something went wrong :( Try again.")
        return


    await state.update_data(url=url)
    await state.set_state(MonitorStates.mode)
    await message.answer("The URL is good, now tell me what you want to track", reply_markup=create_url_state_keyboard(url))


def save_monitor(name, url, mode, user_id):
    user_id = str(user_id)

    monitor = {
        "id": uuid4().hex,
        "name": name,
        "url": url,
        "mode": mode,
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

'''
#################
@create_monitor_form_router.callback_query(MonitorStates.mode)
async def page_changes(query: CallbackQuery, state: FSMContext):
    await state.update_data(mode=query.data)
    await state.set_state(MonitorStates.approval)

    # match query.data:
    #     case "text_change":
    #         text_change.monitoring(user_id=query.from_user.id)
        # case "number_check":
            # number_check.monitoring()


    data = await state.get_data()

    await query.message.edit_text(
        f"Review monitor:\n"
        f"Name: {data['name']}\n"
        f"URL: {data['url']}\n"
        f"Mode: {data['mode']}\n\n"
        f"Create this monitor?",
        reply_markup=create_monitor_approval_keyboard(),
    )
    await query.answer()
##################
'''

@create_monitor_form_router.callback_query(MonitorStates.approval, F.data == "monitor:approve")
async def approve_monitor(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    save_monitor(
        data["name"],
        data["url"],
        data["mode"],
        user_id=query.from_user.id,
    )

    await query.message.edit_text("Monitor created!")
    await state.clear()
    await query.answer()


@create_monitor_form_router.callback_query(MonitorStates.approval, F.data == "monitor:cancel")
async def cancel_monitor(query: CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text("Monitor creation cancelled.")
    await query.answer()