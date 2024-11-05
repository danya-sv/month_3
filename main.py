import asyncio
import logging
from handlers.random import random_router
from handlers.start import start_router
from handlers.myinfo import myinfo_router
from handlers.random_recipe import recipe_router
from bot_config import dp, bot


async def main():
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(random_router)
    dp.include_router(recipe_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
