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

from keybords import show_monitors_keyboard, delete_monitors_keyboard

monitor_router = Router()

def load_monitors(user_id: int) -> list[dict]:
    try:
        with open("monitors.json", "r", encoding="utf-8") as file:
            storage = json.load(file)
    except FileNotFoundError:
        logging.info("Storage is empty")
        return []

    return storage.get(str(user_id), {}).get("monitors", [])

def delete_monitors(user_id: int, monitor_id: str | None = None) -> int:
    try:
        with open("monitors.json", "r", encoding="utf-8") as file:
            storage = json.load(file)
    except FileNotFoundError:
        return 0

    user_data = storage.get(str(user_id), {})
    monitors = user_data.get("monitors", [])

    remaining = (
        [] if monitor_id is None
        else [monitor for monitor in monitors if monitor.get("id") != monitor_id]
    )
    deleted_count = len(monitors) - len(remaining)

    if deleted_count:
        user_data["monitors"] = remaining
        with open("monitors.json", "w", encoding="utf-8") as file:
            json.dump(storage, file, ensure_ascii=False, indent=2)

    return deleted_count

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

#router to choose and delete monitor
@monitor_router.message(Command("delete_monitor"))
async def start_delete_monitor(message: Message):
    monitors = load_monitors(message.from_user.id)

    if not monitors:
        await message.answer("No monitors to delete.")
        return

    await message.answer(
        "Choose a monitor to delete:",
        reply_markup=delete_monitors_keyboard(monitors),
    )
#router for delete all monitors
@monitor_router.callback_query(F.data.startswith("delete:"))
async def delete_callback(callback: CallbackQuery):
    target = callback.data.split(":", 1)[1]
    monitor_id = None if target == "all" else target

    deleted_count = delete_monitors(callback.from_user.id, monitor_id)
    monitors = load_monitors(callback.from_user.id)

    if target == "all":
        text = f"Deleted {deleted_count} monitor(s)."
    elif deleted_count:
        text = "Monitor deleted. Choose another:"
    else:
        text = "Monitor not found."

    keyboard = (
        delete_monitors_keyboard(monitors)
        if monitors and target != "all"
        else None
    )

    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()