from datetime import time, date

from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from loader import dp
from data.config import admin_id
from utils.misc import rate_limit
from keyboards.default import show_keyboard
from states import ProcedureState, WorkdayState
from utils.db_api import ProcedureCRUD, WorkdayCRUD


main_keyboard = [
    "Добавить процедуру",
    "Добавить рабочий день",
    "Показать записи",
    "Удалить рабочие дни",
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
    await state.update_data(name_procedure=name_procedure.capitalize())
    await message.answer("Введите длительность процедуры в формате ЧЧ.ММ:")
    await ProcedureState.next()


@dp.message_handler(state=ProcedureState.Duration)
async def answer_duration(message: Message, state: FSMContext):
    procedure_duration = message.text
    try:
        procedure_duration = procedure_duration.split(".")
        procedure_duration = list(map(int, procedure_duration))
        hours = procedure_duration[0]
        minutes = procedure_duration[1]
        await state.update_data(procedure_duration=time(hour=hours, minute=minutes))
        await message.answer("Введите стоимость процедуры:")
        await ProcedureState.next()
    except:
        await message.answer("Неверное время. Введите длительность процедуры в формате ЧЧ.ММ:")


@dp.message_handler(state=ProcedureState.Cost)
async def answer_cost(message: Message, state: FSMContext):
    data = await state.get_data()
    cost_procedure = int(message.text)
    name_procedure = data.get("name_procedure")
    procedure_duration = data.get("procedure_duration")
    ProcedureCRUD.add_procedure(procedure_name=name_procedure,
                                procedure_duration=procedure_duration,
                                cost=cost_procedure)
    await message.answer(f"Добавлена процедура: {name_procedure} \n"
                         f"Длительностью: {procedure_duration.hour}ч  {procedure_duration.minute}мин\n"
                         f"Стоимостью: {cost_procedure} BYN")
    await state.finish()
    await message.answer("Что вы хотите сделать?",
                         reply_markup=await show_keyboard(main_keyboard)
                         )


@rate_limit(3, 'Добавить рабочий день')
@dp.message_handler(user_id=admin_id, text="Добавить рабочий день", state=None)
async def add_workday_admin(message: Message):
    await message.answer("Введите дату в формате ДД.ММ.ГГГГ:", reply_markup=ReplyKeyboardRemove())
    await WorkdayState.first()


@dp.message_handler(state=WorkdayState.Workday)
async def add_day(message: Message, state: FSMContext):
    workday = message.text

    try:
        workday = list(map(int, (workday.split('.')[::-1])))
        year = workday[0]
        month = workday[1]
        day = workday[2]
        workday = date(year=year, month=month, day=day)
        await state.update_data(workday=workday)
        await message.answer("Введите рабочее время в формате ЧЧ.ММ:")
        await WorkdayState.next()
    except:
        await message.answer("Неверная дата. Введите дату в формате ДД.ММ.ГГГГ:")


@dp.message_handler(state=WorkdayState.Worktime)
async def add_time(message: Message, state: FSMContext):
    data = await state.get_data()
    worktime = message.text
    workday = data.get("workday")
    try:
        worktime = list(map(int, worktime.split('.')))
        hours = worktime[0]
        minutes = worktime[1]
        worktime = time(hours, minutes)
        WorkdayCRUD.add_workday(workday=workday,
                                worktime=worktime
                                )
        await message.answer(f"Добавлен рабочий день: {workday} {worktime}")
        await state.finish()
        await message.answer("Что вы хотите сделать?",
                             reply_markup=await show_keyboard(main_keyboard)
                             )
    except:
        await message.answer("Неверное время. Введите рабочее время в формате ЧЧ.ММ:")


@dp.message_handler(text="Отмена")
async def cancel(message: Message):
    await message.answer("Отмена", reply_markup=ReplyKeyboardRemove())


@rate_limit(3, 'Показать записи')
@dp.message_handler(user_id=admin_id, text="Показать записи")
async def show_registry(message: Message):
    workdays = WorkdayCRUD.get_my_workdays()
    if len(workdays):
        for workday in workdays:
            day = workday[0]
            await message.answer(f"{day.workday} {day.worktime}")
    else:
        await message.answer("Записей нет.")


@rate_limit(3, 'Удалить рабочие дни')
@dp.message_handler(user_id=admin_id, text="Удалить рабочие дни")
async def delete_past_workdays(message: Message):
    day = date.today()
    WorkdayCRUD.delete_workdays_past(day=day)
    await message.answer("Рабочие дни удалены")
    await message.answer("Что вы хотите сделать?",
                         reply_markup=await show_keyboard(main_keyboard)
                         )
        
        
