import random
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import FSInputFile

from bot_config import recipes

recipe_router = Router()


@recipe_router.message(Command("recept"))
async def send_random_recipe(message: types.Message):
    recipe = random.choice(recipes)
    caption = (f"{recipe['name']}:\n"
               f"{recipe['recipe']}")
    photo = FSInputFile(recipe["image_path"])
    await message.answer_photo(photo=photo, caption=caption)
