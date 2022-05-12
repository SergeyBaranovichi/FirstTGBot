import logging

from aiogram import Dispatcher

from data.config import admin_id


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(admin_id, "Бот Запущен и готов к работе")

    except Exception as err:
        logging.exception(err)
