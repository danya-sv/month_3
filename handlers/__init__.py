from aiogram import Router, F


from .start import start_router
from .review_dialog import review_router
from .reg import reg_router
from .random import random_router
from .random_recipe import recipe_router
from .myinfo import myinfo_router
from .menu import menu_router
from .dishes import dishes_router


private_router = Router()
private_router.include_router(start_router)
private_router.include_router(myinfo_router)
private_router.include_router(random_router)
private_router.include_router(recipe_router)
private_router.include_router(review_router)
private_router.include_router(reg_router)
private_router.include_router(dishes_router)
private_router.include_router(menu_router)


private_router.message.filter(F.chat.type == "private")
private_router.callback_query.filter(F.chat.type == "private")