from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from utils.misc import rate_limit
from keyboards.default import show_keyboard
from keyboards.inline import keyboard_for_procedures, keyboard_for_workdays, keyboard_for_confirmation
from states import SignUp
from utils.db_api import ProcedureCRUD, WorkdayCRUD, UserCRUD

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
    await message.answer("Выберите процедуру:",
                         reply_markup=await keyboard_for_procedures(ProcedureCRUD.get_all_procedures())
                         )
    # await message.answer("Выберите процедуру:", reply_markup=await show_keyboard(orders))
    await SignUp.first()


# Через колбэк и инлайн клавиатуру
@dp.callback_query_handler(state=SignUp.ChooseProcedure)
async def choose_procedure(callback: CallbackQuery, state: FSMContext):
    procedure_id = int(callback.data)
    procedure = ProcedureCRUD.get_procedure_by_id(procedure_id).procedure_name
    await state.update_data(procedure=procedure)
    await state.update_data(procedure_id=procedure_id)
    await callback.message.answer("Когда:",
                                  reply_markup=await keyboard_for_workdays(WorkdayCRUD.get_workdays())
                                  )
    await SignUp.next()


# Через хэндлер и обычную клавиатуру
# @dp.message_handler(state=SignUp.ChooseProcedure)
# async def choose_procedure(message: Message, state: FSMContext):
#     procedure = message.text
#     await state.update_data(procedure=procedure)
#     await message.answer("Когда:", reply_markup=await show_keyboard(days))
#     await SignUp.next()


# Через колбэк и инлайн клавиатуру
@dp.callback_query_handler(state=SignUp.ChooseDay)
async def choose_day(callback: CallbackQuery, state: FSMContext):
    workday_id = int(callback.data)
    day = WorkdayCRUD.get_workday_by_id(workday_id)
    worktime = day.worktime
    workday = day.workday
    await state.update_data(day=f"{workday} {worktime}")
    await state.update_data(workday_id=workday_id)
    data = await state.get_data()
    procedure = data.get("procedure")
    await callback.message.answer(f"Вы выбрали {procedure} на {workday} {worktime}\n"
                                  f"Вы подтверждаете запись?",
                                  reply_markup=await keyboard_for_confirmation())
    await SignUp.next()



# Через хэндлер и обычную клавиатуру
# @dp.message_handler(state=SignUp.ChooseDay)
# async def choose_day(message: Message, state: FSMContext):
#     day = message.text
#     await state.update_data(day=day)
#     data = await state.get_data()
#     procedure = data.get("procedure")
#     await message.answer(f"Вы выбрали {procedure} на {day}\n"
#                          f"Вы подтверждаете запись?", reply_markup=await show_keyboard([
#         "Да",
#         "Нет"
#     ]))
#     await SignUp.next()


# Через колбэк и инлайн клавиатуру
@dp.callback_query_handler(state=SignUp.Confirmation)
async def confirmation(callback: CallbackQuery, state: FSMContext):
    if callback.data == "Да":
        data = await state.get_data()
        print(data.get("workday_id"))
        try:
            user = {
                "first_name": callback.from_user.first_name,
                "tg_id": callback.from_user.id,
                # "phonenumber": "+3755554456565",
                "procedure_id": data["procedure_id"],
                "workday_id": data["workday_id"],
            }
            UserCRUD.add_user(user)
            await callback.message.answer("Спасибо!")
            WorkdayCRUD.update_workday_by_id(workday_id=data.get("workday_id"), availability=False)
        except:
            await callback.message.answer("Только одна запись!!!")

    elif callback.data == "Нет":
        await callback.message.answer("Ну ладно((")
    await state.finish()


# Через хэндлер и обычную клавиатуру
# @dp.message_handler(text="Да", state=SignUp.Confirmation)
# async def confirmation(message: Message, state: FSMContext):
#     await message.answer("Спасибо!", reply_markup=ReplyKeyboardRemove())
#     await state.finish()


# Через хэндлер и обычную клавиатуру
# @dp.message_handler(text="Нет", state=SignUp.Confirmation)
# async def confirmation(message: Message, state: FSMContext):
#     await message.answer("Ну ладно((", reply_markup=ReplyKeyboardRemove())
#     await state.finish()


@dp.message_handler(text="Отмена", state=SignUp)
async def cancel(message: Message, state: FSMContext):
    await message.answer("Отмена", reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(text="Отменить запись")
async def cancel_record(message: Message):
    user = UserCRUD.get_user_by_tgid(message.from_user.id)
    if user:
        workday_id = user.workday_id
        WorkdayCRUD.update_workday_by_id(workday_id=workday_id, availability=True)
        UserCRUD.delete_user_by_tg_id(message.from_user.id)
        await message.answer("Ваша запись отменена")
    else:
        await message.answer("Ты дурак? Ты же не записывался")
