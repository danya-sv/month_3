import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import dotenv_values
import random

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()
names = ["Иван", "Мария", "Алексей", "Ольга", "Дмитрий"]
user_ids = set()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_ids.add(user_id)
    user_count = len(user_ids)
    name = message.from_user.first_name
    await message.answer(f"Привет, {name}!\n"
                             f"Наш бот обслуживает уже {user_count} пользователей.\n"
                             f"Что умеет бот:\n"
                             f"/start - Начать работу\n"
                             f"/myinfo - Информация о позьзователе\n"
                             f"/random - Случайное имя из списка")

@dp.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    your_id = message.from_user.id
    f_name = message.from_user.first_name
    use_name = message.from_user.username
    await message.answer(f'Ваш id - {your_id}\n'
                         f'Ваше имя - {f_name.title()} \n'
                         f'Ваш username - {use_name}')

@dp.message(Command('random'))
async def random_handler(message: types.Message):
    random_name = random.choice(names)
    await message.answer(f'Рандомное имя из списка - {random_name}')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



