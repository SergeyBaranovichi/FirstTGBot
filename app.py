from utils.set_bot_commands import set_default_commands

# from models import Base
# from loader import engine
# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)


async def on_startup(dp):
    import filters
    import middlewares
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
