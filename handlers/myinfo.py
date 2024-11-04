from aiogram import types, Router
from aiogram.filters import Command

myinfo_router = Router()


@myinfo_router.message(Command("myinfo"))
async def myinfo_handler(message: types.Message):
    your_id = message.from_user.id
    f_name = message.from_user.first_name
    use_name = message.from_user.username
    await message.answer(f'Ваш id - {your_id}\n'
                         f'Ваше имя - {f_name.title()} \n'
                         f'Ваш username - {use_name}')
