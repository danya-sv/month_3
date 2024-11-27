from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from bot_config import BAD_WORDS


group_router = Router()




@group_router.message(Command("ban", prefix="!"))
async def ban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение, которое хотите забанить.")
    else:
        id = message.reply_to_message.from_user.id
        await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=id)


@group_router.message(Command("unban", prefix="!"))
async def unban_user(message: types.Message):
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение пользователя, чтобы снять ограничения.")
    else:
        id = message.reply_to_message.from_user.id
        await message.bot.restrict_chat_member(
            chat_id=message.chat.id,
            user_id=id,
            permissions=ChatPermissions(can_send_messages=True)  # Разрешаем отправку сообщений
        )
        await message.answer(f"Пользователь {message.reply_to_message.from_user.full_name} снова активен.")
        
        

@group_router.message(F.text)
async def check_for_bad_words(message: types.Message):
    message_text = message.text.lower()

    for word in BAD_WORDS:
        if word in message_text:
            user_id = message.from_user.id
            await message.bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=user_id,
                permissions=ChatPermissions(can_send_messages=False)
            )
            await message.answer(
                f"Пользователь {message.from_user.full_name} ограничен за использование запрещённых слов."
            )
            break

