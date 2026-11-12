import json

from aiogram import Router
from aiogram.types import Message

text_change_route = Router()

MONITORING_TYPE = "text_change"


def monitoring(user_id, ):
    with open("monitors.json", "r", encoding="utf-8") as file:
        tc_monitors = json.load(file)



@text_change_route.message
async def notify(message: Message):
    await message.answer("")