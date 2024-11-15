from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

from database.database import Database

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()
names = ["Иван", "Мария", "Алексей", "Ольга", "Дмитрий"]
user_ids = set()
reviewed_users = set()
recipes = [
    {
        "name": "Паста Карбонара",
        "recipe": "Варим спагетти, добавляем обжаренный бекон, яйца и сыр Пекорино.",
        "image_path": "resipes/pasta.jpg",
    },
    {
        "name": "Салат Цезарь",
        "recipe": "Смешиваем листья салата, курицу, сухарики, добавляем соус Цезарь и посыпаем пармезаном.",
        "image_path": "resipes/salat.jpg",
    },
    {
        "name": "Борщ",
        "recipe": "Варим бульон, добавляем свёклу, капусту, картофель, морковь и томатную пасту. Подаём со сметаной.",
        "image_path": "resipes/borsch.jpg",
    },
    {
        "name": "Том Ям",
        "recipe": "Варим креветки в кокосовом молоке с пастой Том Ям, добавляем грибы, лемонграсс и лайм.",
        "image_path": "resipes/tomyam.jpg",
    },
    {
        "name": "Омлет с овощами",
        "recipe": "Взбиваем яйца с солью и перцем, добавляем обжаренные овощи (помидоры, перец, шпинат), жарим до готовности.",
        "image_path": "resipes/omlet.jpg",
    },
    {
        "name": "Чизкейк",
        "recipe": "Смешиваем сливочный сыр с сахаром и яйцами, заливаем на основу из печенья, выпекаем в духовке.",
        "image_path": "resipes/cheesecake.jpg",
    },
]
reg_account = set()
registered_users = {}
reg_users = {}
database = Database("datab.sqlite")
