import asyncio
import json
import logging
import ssl

import aiohttp
import certifi
from aiogram import Router, F
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bs4 import BeautifulSoup

from handlers.states import MonitorStates, MonitoringTextStates
from keybords import choose_one_text
from text import number_emojis

text_change_router = Router()

MONITORING_TYPE = "text_change"

def normalize(text):
    return " ".join(text.split()).casefold()

# def monitoring(user_id):
#     with open("monitors.json", "r", encoding="utf-8") as file:
#         tc_monitors = json.load(file)[user_id]["monitors"]

@text_change_router.callback_query(MonitorStates.mode, F.data == MONITORING_TYPE)
async def mode_setting_start(query: CallbackQuery, state: FSMContext):
    await state.update_data(mode=query.data)

    await query.message.answer("What text is it gonna be?")

    await state.set_state(MonitoringTextStates.target)


@text_change_router.message(MonitoringTextStates.target)
async def target_processing(message: Message, state: FSMContext):
    data = await state.get_data()
    normalized_msg = normalize(message.text.strip())

    try:
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context)

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(data["url"]) as response:
                response.raise_for_status()
                html = await response.text()

    except (aiohttp.ClientError, asyncio.TimeoutError) as err:
        logging.error(err)
        await message.reply("Something went wrong :( Try again.")
        return


    soup = BeautifulSoup(html, "html.parser")

    matches = soup.find_all(
        string=lambda a: a and normalized_msg in normalize(a)
    )

    matches_len = len(matches)
    if matches_len > 1:
        msg = ""
        for i, text in enumerate(matches, start=1):
            msg += f"{number_emojis[i]} {text.string}"

        await message.answer(msg, reply_markup=choose_one_text(matches_len))


        
        
        
@text_change_router.callback_query(MonitoringTextStates.target, F.data.startswith("choose_text:"))
async def choose_one_text_callback(query: CallbackQuery, state: FSMContext):
    callback_answer = query.data.split(":", maxsplit=3)[2]

    if query.data == "another":
        pass
        # Handle option "another" by creating new state
        # return
    else:
        await state.update_data(choose_text=callback_answer)