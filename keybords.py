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