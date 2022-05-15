from aiogram import types
from loader import dp


@dp.message_handler()
async def bot_echo(message: types.Message):
    pass
    # print(message)
    # await message.answer(message.text)
