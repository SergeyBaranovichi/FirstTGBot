from aiogram.dispatcher.filters.state import StatesGroup, State


class ProcedureState(StatesGroup):
    Name = State()
    Duration = State()
    Cost = State()


class WorkdayState(StatesGroup):
    Workday = State()
    Worktime = State()
