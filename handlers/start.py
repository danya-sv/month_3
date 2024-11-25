from aiogram import Router, types
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
                types.InlineKeyboardButton(text="Наш сайт", url="https://geeks.kg/"),
            ],
            [types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review")],
            [types.InlineKeyboardButton(text="Регистрация", callback_data="reg")],
            [types.InlineKeyboardButton(text="Меню", callback_data="menu")],
            [types.InlineKeyboardButton(text="Добавить блюдо", callback_data="add_dish")],
            [types.InlineKeyboardButton(text="Добавить Категорию", callback_data="add_category")],
        ]
    )

    await message.answer(
        f"Привет, {name}! 👋\n\n"
        f"Добро пожаловать в Telegram-бота для нашего TG Restoran. Уже {user_count} пользователей доверили нам свое время! 🚀\n\n"
        f"Вот что может наш бот:\n"
        f"🔹 /start — Перезапустить работу с ботом\n"
        f"🔹 /myinfo — Узнать информацию о вашем профиле\n"
        f"🔹 /recept — Подобрать случайный рецепт 🍽️\n"
        f"🔹 /random — Получить случайное имя из списка 🎲\n\n"
        f"Используйте меню ниже, чтобы изучить возможности! 👇",
        reply_markup=kb,
    )
