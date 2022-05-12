from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def keyboard_for_procedures(procedures: list) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[[InlineKeyboardButton(
            text=f"{procedure[0].procedure_name}/n"
                 f"Длительность: {procedure[0].procedure_duration.hour} {procedure[0].procedure_duration.minute}/n"
                 f"Цена: {procedure[0].cost} BYN",
            callback_data=procedure[0].id
        )] for procedure in procedures]
    )
    return keyboard


async def keyboard_for_workdays(workdays: list) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        row_width=1,
        inline_keyboard=[[InlineKeyboardButton(
            text=f"{workday[0].workday} {workday[0].worktime}",
            callback_data=workday[0].id
        )] for workday in workdays]
    )
    return keyboard


async def keyboard_for_confirmation() -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [InlineKeyboardButton(text="Да", callback_data="Да")],
            [InlineKeyboardButton(text="Нет", callback_data="Нет")]
        ]
    )
    return keyboard
