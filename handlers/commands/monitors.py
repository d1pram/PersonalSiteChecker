import json
from pathlib import Path

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


monitor_router = Router()


DATA_FILE = Path(__file__).resolve().parents[2] / "monitors.json"

PAGE_SIZE = 3

def load_monitors(user_id: int) -> list[dict]:
    # if not DATA_FILE.exists():
    #     return []
    #
    # data = json.loads(DATA_FILE.read.text(encoding="utf-8"))
    #
    # return data.get(str(user_id), {}).get("monitors", [])

    try:
        with open("monitors.json", "r", encoding="utf-8") as file:
            # storage = json.load(file).get(str(user_id), {}).get("monitors", [])
            storage = json.load(file)[str(user_id)]["monitors"]
    except FileNotFoundError:
        storage = {}

    return storage

def make_keyboard(monitors: list[dict], page: int):

    page_count = max(1, (len(monitors)+ PAGE_SIZE -1) // PAGE_SIZE)

    page = max(0, min(page, page_count - 1))

    start = page * PAGE_SIZE
    visible_monitors = monitors[start : start + PAGE_SIZE]

    rows = [
        [
            InlineKeyboardButton(
                text=monitor.get("name", "Without name"),
                url=monitor["url"],
            )
        ]
        for monitor in visible_monitors
    ]

    navigation = [] #adding arrows for pages

    if page > 0:
        navigation.append(
            InlineKeyboardButton(
                text="←",
                callback_data=f"monitors:page:{page - 1}"
            )
        )

    if page < page_count - 1:
        navigation.append(
            InlineKeyboardButton(
                text="→",
                callback_data = f"monitors:page:{page + 1}"
            )
        )
    if navigation:
        rows.append(navigation)

    keyboard = InlineKeyboardMarkup(inline_keyboard=rows)

    return keyboard, page, page_count

@monitor_router.message(Command("monitors"))
async def show_monitors(message: Message):
    """Processes /monitors and show the first page of the website"""

    monitors = load_monitors(message.from_user.id)

    if not monitors:
        await  message.answer("No monitors yet")
        return

    keyboard, page, page_count = make_keyboard(monitors, 0)

    await message.answer(
        f"Your monitors - page {page + 1}/{page_count}",
        reply_markup=keyboard,
    )

@monitor_router.callback_query(F.data.startwith("monitors:page:"))
async def change_page(callback: CallbackQuery):

    page = int(callback.data.rsplit(":", 1)[1])

    monitors = load_monitors(callback.from_user.id)

    keyboard, page, page_count = make_keyboard(monitors, page)

    await callback.message.edit_text(
        f"Your monitors - page {page + 1}/{page_count}",
        reply_markup=keyboard,
    )

    await callback.answer()