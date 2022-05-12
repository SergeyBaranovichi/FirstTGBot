from aiogram.dispatcher.filters.state import StatesGroup, State


class SignUp(StatesGroup):
    ChooseProcedure = State()
    ChooseDay = State()
    Confirmation = State()
