import random
from aiogram import types, Router
from aiogram.filters import Command
from bot_config import names

random_router = Router()


@random_router.message(Command('random'))
async def random_handler(message: types.Message):
    random_name = random.choice(names)
    await message.answer(f'Рандомное имя из списка - {random_name}')
