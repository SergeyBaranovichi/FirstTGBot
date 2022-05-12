from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def show_keyboard(buttons: list) -> ReplyKeyboardMarkup:
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        one_time_keyboard=False,
        resize_keyboard=True,
        row_width=1,
        keyboard=[[KeyboardButton(text=f"{button}")] for button in buttons]
    )
    return keyboard
