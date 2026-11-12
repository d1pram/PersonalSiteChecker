import asyncio
import json
import logging
import ssl

import aiohttp
import certifi
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from bs4 import BeautifulSoup

from handlers.states import MonitorStates, MonitoringStates

text_change_route = Router()

MONITORING_TYPE = "text_change"

def normalize(text):
    return " ".join(text.split()).casefold()

# def monitoring(user_id):
#     with open("monitors.json", "r", encoding="utf-8") as file:
#         tc_monitors = json.load(file)[user_id]["monitors"]

@text_change_route.callback_query(MonitorStates.mode, F.data == MONITORING_TYPE)
async def mode_setting_start(query: CallbackQuery, state: FSMContext):
    await state.update_data(mode=query.data)

    await query.message.answer("What text is it gonna be?")

    await state.set_state(MonitoringStates.target)


@text_change_route.message(MonitoringStates.target)
async def target_processing(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = normalize(message.text.strip())

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
        string=lambda text: text and msg in normalize(text)
    )

    print(msg in soup.get_text())
    print(msg)
    print(matches)