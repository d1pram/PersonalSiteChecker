from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from aiogram.types import DisabledButton, InlineKeyboardButton

PAGE_SIZE = 4
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

    for monitor in visible_monitors:
        builder.button(
            text=monitor.get("name"),
            callback_data=f"monitor:{monitor['id']}",
        )
    layouts = {1: (1,), 2: (2,), 3: (2,1), 4: (2,2),}

    if visible_monitors:
        builder.adjust(*layouts[len(visible_monitors)])

    navigation = [] #collect only available arrows

    if page > 0:
        navigation.append(
            InlineKeyboardButton(
                text="←",
                callback_data=f"monitors:page:{page - 1}",
            )
        )

    if page < page_count - 1:
        navigation.append(
            InlineKeyboardButton(
                text="→",
                callback_data=f"monitors:page:{page + 1}",
            )
        )


    if navigation:
        builder.row(*navigation)

    return builder.as_markup(), page, page_count


def delete_monitors_keyboard(monitors: list[dict]):
    builder = InlineKeyboardBuilder()

    for monitor in monitors:
        builder.button(
            text=f"🗑{monitor.get('name')}",
            callback_data=f"delete:{monitor['id']}",
        )
    builder.adjust(1)

    if monitors:
        builder.row(
            InlineKeyboardButton(
                text="Delete all",
                callback_data="delete:all",
            )
        )

    return builder.as_markup()