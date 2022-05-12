from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.misc import rate_limit
from keyboards.default import show_keyboard
from states import SignUp

orders = [
    "Процедура 1",
    "Процедура 2",
    "Процедура 3",
    "Процедура 4",
    "Процедура 5",
]

days = [
    "20.05.2022 17:15",
    "21.05.2022 17:15",
    "22.05.2022 17:15",
    "23.05.2022 17:15",
]


@dp.message_handler(Command("start"))
async def start(message: Message):
    await message.answer("Начать", reply_markup=await show_keyboard([
        "Записаться",
        "Отменить запись",
        "Отмена",
    ]))


@dp.message_handler(text="Записаться", state=None)
async def sign_up(message: Message):
    await message.answer("Выберите процедуру:", reply_markup=await show_keyboard(orders))
    await SignUp.first()


@dp.message_handler(state=SignUp.ChooseProcedure)
async def choose_procedure(message: Message, state: FSMContext):
    procedure = message.text
    await state.update_data(procedure=procedure)
    await message.answer("Когда:", reply_markup=await show_keyboard(days))
    await SignUp.next()


@dp.message_handler(state=SignUp.ChooseDay)
async def choose_day(message: Message, state: FSMContext):
    day = message.text
    await state.update_data(day=day)
    data = await state.get_data()
    procedure = data.get("procedure")
    await message.answer(f"Вы выбрали {procedure} на {day}\n"
                         f"Вы подтверждаете запись?", reply_markup=await show_keyboard([
        "Да",
        "Нет"
    ]))
    await SignUp.next()


@dp.message_handler(text="Да", state=SignUp.Confirmation)
async def confirmation(message: Message, state: FSMContext):
    await message.answer("Спасибо!", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(text="Нет", state=SignUp.Confirmation)
async def confirmation(message: Message, state: FSMContext):
    await message.answer("Ну ладно((", reply_markup=ReplyKeyboardRemove())
    await state.finish()
