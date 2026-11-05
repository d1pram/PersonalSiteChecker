import asyncio
import logging

import aiohttp
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

create_monitor_form_router = Router()

class MonitorStates(StatesGroup):
    name = State()
    url = State()
    purpose = State()


@create_monitor_form_router.message(Command("create_monitor"))
async def command_start(message: Message, state: FSMContext) :
    await state.set_state(MonitorStates.name)
    await message.answer(
        "Hi there! So how should this monitor be called?",
        reply_markup=ReplyKeyboardRemove(),
    )

@create_monitor_form_router.message(MonitorStates.name)
async def process_name(message: Message, state: FSMContext) :
    await state.update_data(name=message.text)
    await state.set_state(MonitorStates.url)
    await message.answer("Okay good, now you can type your URL:\n|| Include http:// or https:// ||")


@create_monitor_form_router.message(MonitorStates.url)
async def process_url(message: Message, state: FSMContext):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(message.text) as response:
                response.raise_for_status()
    except (aiohttp.ClientConnectionError, asyncio.TimeoutError) as err:
        logging.error(err)
        await message.reply("Something went wrong :( Try again.")
        await asyncio.sleep(1.5)
        await state.set_state(MonitorStates.url)


    keyboard_builder = InlineKeyboardBuilder().adjust(1,3)

    keyboard_builder.row(
        InlineKeyboardButton(text="Open my page", url=message.text),
        InlineKeyboardButton(text="Number check", callback_data="number_check"),
        InlineKeyboardButton(text="Changes in page", callback_data="page_changes"),
    )

    await state.update_data(url=message.text)
    await state.set_state(MonitorStates.purpose)
    await message.answer("The URL is good, now tell me what you want to track", reply_markup=keyboard_builder.as_markup())


@create_monitor_form_router.callback_query(state=MonitorStates.purpose)
async def page_changes(state: FSMContext, query: CallbackQuery):
    await state.update_data(query.data)

    if query.data == "number_check":
        await query.answer(show_alert=True, text="Number check mode is set.\nTo see more details do «/help Number check»")
    elif query.data == "page_changes":
        await query.answer(show_alert=True, text="Changes in page mode is set.\nTo see more details do «/help Changes in page»")


