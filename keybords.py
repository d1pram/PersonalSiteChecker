from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_url_state_keyboard(url: str):
    url_state_keyboard = InlineKeyboardBuilder().adjust(1,3)

    url_state_keyboard.row(
        InlineKeyboardButton(text="Open my page", url=url),
        InlineKeyboardButton(text="Number check", callback_data="number_check"),
        InlineKeyboardButton(text="Changes in page", callback_data="page_changes"),
        )

    return url_state_keyboard.as_markup()

def create_monitor_approval_keyboard():
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text="Confirm",
            callback_data="monitor:approve",
        ),
        InlineKeyboardButton(
            text="Cancel",
            callback_data="monitor:cancel",
        ),
    )

    return keyboard.as_markup()
