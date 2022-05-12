from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp
from data.config import admin_id
from utils.misc import rate_limit
from keyboards.default import show_keyboard
from states import ProcedureState, WorkdayState

orders = [
    "процедура 1: 13.05.2022 на 17:15",
    "процедура 2: 14.05.2022 на 20:15",
    "процедура 3: 15.05.2022 на 21:15",
]

main_keyboard = [
    "Добавить процедуру",
    "Добавить рабочий день",
    "Показать записи",
    "Отмена",
]


@rate_limit(3, 'menu')
@dp.message_handler(user_id=admin_id, commands=["menu"])
async def show_menu(message: Message):
    await message.answer("Что вы хотите сделать?",
                         reply_markup=await show_keyboard(main_keyboard)
                         )


@rate_limit(3, 'Добавить процедуру')
@dp.message_handler(user_id=admin_id, text="Добавить процедуру", state=None)
async def add_procedure_admin(message: Message):
    await message.answer("Введите название процедуры:", reply_markup=ReplyKeyboardRemove())
    await ProcedureState.first()


@dp.message_handler(state=ProcedureState.Name)
async def answer_name(message: Message, state: FSMContext):
    name_procedure = message.text
    # async with state.proxy() as data:
    #     data["name_procedure"] = name_procedure
    await state.update_data(name_procedure=name_procedure.capitalize())
    await message.answer("Введите длительность процедуры:")
    await ProcedureState.next()


@dp.message_handler(state=ProcedureState.Duration)
async def answer_duration(message: Message, state: FSMContext):
    duration_procedure = message.text
    # async with state.proxy() as data:
    #     data["duration_procedure"] = duration_procedure
    await state.update_data(duration_procedure=duration_procedure)
    await message.answer("Введите стоимость процедуры:")
    await ProcedureState.next()


@dp.message_handler(state=ProcedureState.Cost)
async def answer_cost(message: Message, state: FSMContext):
    data = await state.get_data()
    cost_procedure = int(message.text)
    name_procedure = data.get("name_procedure")
    duration_procedure = data.get("duration_procedure")
    # ProcedureCRUD.add_procedure(procedure_name=name_procedure,
    #                             procedure_duration=duration_procedure,
    #                             cost=cost_procedure)
    await message.answer(f"Добавлена процедура: {name_procedure} \n"
                         f"Длительностью: {duration_procedure} \n"
                         f"Стоимостью: {cost_procedure} BYN")
    await state.finish()
    await message.answer("Что вы хотите сделать?",
                         reply_markup=await show_keyboard(main_keyboard)
                         )


@rate_limit(3, 'Добавить рабочий день')
@dp.message_handler(user_id=admin_id, text="Добавить рабочий день", state=None)
async def add_workday_admin(message: Message):
    await message.answer("Введите дату в формате ГГГГ.ММ.ДД:", reply_markup=ReplyKeyboardRemove())
    await WorkdayState.first()


@dp.message_handler(state=WorkdayState.Workday)
async def add_day(message: Message, state: FSMContext):
    workday = message.text
    # async with state.proxy() as data:
    #     data["name_procedure"] = name_procedure
    await state.update_data(workday=workday)
    await message.answer("Введите рабочее время в формате ЧЧ.ММ:")
    await WorkdayState.next()


@dp.message_handler(state=WorkdayState.Worktime)
async def add_time(message: Message, state: FSMContext):
    data = await state.get_data()
    worktime = message.text
    workday = data.get("workday")
    # ProcedureCRUD.add_procedure(procedure_name=name_procedure,
    #                             procedure_duration=duration_procedure,
    #                             cost=cost_procedure)
    await message.answer(f"Добавлен рабочий день: {workday} {worktime}")
    await state.finish()
    await message.answer("Что вы хотите сделать?",
                         reply_markup=await show_keyboard(main_keyboard)
                         )


@dp.message_handler(text="Отмена")
async def cancel(message: Message):
    await message.answer("Отмена", reply_markup=ReplyKeyboardRemove())


@rate_limit(3, 'Показать записи')
@dp.message_handler(user_id=admin_id, text="Показать записи")
async def show_registry(message: Message):
    for order in orders:
        await message.answer(f"{order}")
