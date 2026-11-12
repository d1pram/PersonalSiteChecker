from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import DisabledButton, InlineKeyboardButton

from text import number_emojis

PAGE_SIZE = 3
MONITORING_MODES = {"Number check": "number_check", "Changes in page" : "page_changes", "Text change": "text_change"}

def create_url_state_keyboard(url: str):
    url_state_keyboard = InlineKeyboardBuilder()

    url_state_keyboard.add(InlineKeyboardButton(text="Open my page", url=url))

    for mode in MONITORING_MODES.keys():
        url_state_keyboard.add(InlineKeyboardButton(text=mode, callback_data=MONITORING_MODES[mode]))

    return url_state_keyboard.adjust(1,3).as_markup()

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

def show_monitors_keyboard(monitors: list[dict], page: int):
    page_count = max(1, (len(monitors) + PAGE_SIZE - 1) // PAGE_SIZE)

    page = max(0, min(page, page_count - 1))

    start = page * PAGE_SIZE
    visible_monitors = monitors[start : start + PAGE_SIZE]

    builder = InlineKeyboardBuilder()

    builder.adjust(1)
    for monitor in visible_monitors:
        builder.button(text=monitor.get("name"), callback_data=f"monitor:['id']")

    builder.adjust(1)

    # When pages < 4 no arrows and dynamic changes of buttons
    if page == 0:
        left_button = InlineKeyboardButton(
            text="←",
            disabled=DisabledButton(),
        )
    else:
        left_button = InlineKeyboardButton(
            text="←",
            callback_data=f"monitors:page:{page - 1}",
        )

    if page == page_count - 1:
        right_button = InlineKeyboardButton(
            text="→",
            disabled=DisabledButton(),
        )
    else:
        right_button = InlineKeyboardButton(
            text="→",
            callback_data=f"monitors:page:{page + 1}",
        )

    builder.row(left_button, right_button)

    return builder.as_markup(), page, page_count

def choose_one_text(number_of_buttons):
    builder = InlineKeyboardBuilder()

    for i in range(number_of_buttons):
        builder.button(text=f"{number_emojis[i+1]}", callback_data=f"choose_text:{i}")

    builder.adjust(3)

    builder.button(text="🔙 Choose another text", callback_data="choose_text:another")
    return builder.as_markup()

#Create keyboard for when entering monitoring mode to be able to go back and change it