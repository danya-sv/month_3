import asyncio
import logging

from bot_config import bot, database, dp
from handlers.dishes import dishes_router
from handlers.menu import menu_router
from handlers.myinfo import myinfo_router
from handlers.random import random_router
from handlers.random_recipe import recipe_router
from handlers.reg import reg_router
from handlers.review_dialog import review_router
from handlers.start import start_router


async def on_startup(bot):
    database.create_tables()
    # database.clear_dishes() """Юзал для очистки таблиц"""


async def main():
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(random_router)
    dp.include_router(recipe_router)
    dp.include_router(review_router)
    dp.include_router(reg_router)
    dp.include_router(dishes_router)
    dp.include_router(menu_router)
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
