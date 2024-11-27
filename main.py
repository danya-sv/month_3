import asyncio
import logging

from bot_config import bot, database, dp
from handlers import private_router
from handlers.group import group_router


async def on_startup(bot):
    database.create_tables()
    # database.clear_dishes() """Юзал для очистки таблиц"""


async def main():
    dp.include_router(private_router)
    dp.include_router(group_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
