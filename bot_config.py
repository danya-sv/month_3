from aiogram import Bot, Dispatcher
from dotenv import dotenv_values

token = dotenv_values(".env")["BOT_TOKEN"]
bot = Bot(token=token)
dp = Dispatcher()
names = ["Иван", "Мария", "Алексей", "Ольга", "Дмитрий"]
user_ids = set()
