import json
import logging
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from keybords import show_monitors_keyboard

monitor_router = Router()

def load_monitors(user_id: int) -> list[dict]:
    try:
        with open("monitors.json", "r", encoding="utf-8") as file:
            storage = json.load(file)[str(user_id)]["monitors"]
    except FileNotFoundError:
        logging.info("Storage is empty")
        storage = {}

    return storage

@monitor_router.message(Command("monitors"))
async def show_monitors(message: Message):

    monitors = load_monitors(message.from_user.id)

    if not monitors:
        await  message.answer("No monitors yet")
        return

    keyboard, page, page_count = show_monitors_keyboard(monitors, 0)

    await message.answer(
        f"Your monitors - page {page + 1}/{page_count}",
        reply_markup=keyboard,
    )

@monitor_router.callback_query(F.data.startswith("monitors:page:"))
async def change_page(callback: CallbackQuery):

    page = int(callback.data.rsplit(":", 2)[2])

    monitors = load_monitors(callback.from_user.id)

    keyboard, page, page_count = show_monitors_keyboard(monitors, page)

    await callback.message.edit_text(
        f"Your monitors - page {page + 1}/{page_count}",
        reply_markup=keyboard,
    )

    await callback.answer()