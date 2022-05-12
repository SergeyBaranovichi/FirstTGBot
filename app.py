from utils.set_bot_commands import set_default_commands

from utils.db_api import Base
from utils.db_api import engine


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

    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
    executor.start_polling(dp, on_startup=on_startup)
