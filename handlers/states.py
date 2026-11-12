from aiogram.fsm.state import StatesGroup, State


class MonitoringTextStates(StatesGroup):
    target = State()
    choose_text = State()
    interval = State()


class MonitorStates(StatesGroup):
    name = State()
    url = State()
    mode = State()
    approval = State()
