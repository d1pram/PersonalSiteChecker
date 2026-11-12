from aiogram.fsm.state import StatesGroup, State


class MonitoringStates(StatesGroup):
    target = State()
    interval = State()


class MonitorStates(StatesGroup):
    name = State()
    url = State()
    mode = State()
    approval = State()
