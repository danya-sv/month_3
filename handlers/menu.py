from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot_config import database

menu_router = Router()

@menu_router.callback_query(F.data == "menu")
async def view_all_dishes(callback: CallbackQuery):
    await callback.answer()
    all_dish = database.fetch(
        query="""
            SELECT dishes.name, dishes.price, dish_categories.name AS category
            FROM dishes
            JOIN dish_categories ON dishes.category_id = dish_categories.id
            ORDER BY dishes.price ASC
            """
    )

    response = "🍽️ Наше меню:\n\n"
    for dish in all_dish:
        response += (
            f"📝 Название: {dish['name']}\n"
            f"💵 Цена: {dish['price']} сом\n"
            f"📋 Категория: {dish['category']}\n\n"
        )
    await callback.message.answer(response)
