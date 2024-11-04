from aiogram import types, Router
from aiogram.filters import Command
from bot_config import user_ids

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_ids.add(user_id)
    user_count = len(user_ids)
    name = message.from_user.first_name

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш inst", url="https://www.instagram.com/geeks_edu/"
                ),
                types.InlineKeyboardButton(
                    text="Наш сайт", url="https://geeks.kg/"
                )
            ]
        ]
    )

    await message.answer(f"Привет, {name}!\n"
                         f"Наш бот обслуживает уже {user_count} пользователей.\n"
                         f"Что умеет бот:\n"
                         f"/start - Начать работу\n"
                         f"/myinfo - Информация о позьзователе\n"
                         f"/random - Случайное имя из списка", reply_markup=kb)
