from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery

from bot_config import reg_account, reg_users, registered_users, reviewed_users

review_router = Router()


class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()
    total_rating = State()


def main_kb():
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="5")],
            [types.KeyboardButton(text="4")],
            [types.KeyboardButton(text="3")],
            [types.KeyboardButton(text="2")],
            [types.KeyboardButton(text="1")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def cleanliness_keyboard():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Очень чисто", callback_data="Очень чисто"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Средне чисто", callback_data="Средне чисто"
                )
            ],
            [types.InlineKeyboardButton(text="Грязно", callback_data="Грязно")],
        ]
    )


""" Функцию создал, чтобы в коде не дублировать клавиатуру """


@review_router.callback_query(F.data == "review")
async def start_review(callback: CallbackQuery, state: FSMContext):
    id_user = callback.from_user.id
    if id_user not in reg_account:
        await callback.message.answer(
            "Чтобы оставить отзыв, пожалуйста, зарегистрируйтесь!"
        )
        await callback.answer()
        await state.clear()
        return

    if id_user in reviewed_users:
        await callback.message.answer("Вы уже оставляли отзыв!")
        await callback.answer()
        await state.clear()
    else:
        reviewed_users.add(id_user)
        await callback.answer()  # чтобы кнопка не мигала
        await state.set_state(RestaurantReview.name)

    name_kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=registered_users[id_user])]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await callback.message.answer("Напишите ваше имя", reply_markup=name_kb)


@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_number)
    id_u = message.from_user.id
    phone_kb = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=reg_users[id_u])]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    await message.answer(
        "Напишите ваш номер телефона\nИспользуйте формат +996, +7 и т.д.",
        reply_markup=phone_kb,
    )


@review_router.message(RestaurantReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    code_num = ["+996", "+7", "+33", "+49", "+39", "+44", "+1"]
    for code in code_num:
        if message.text.startswith(code):
            await state.update_data(phone_number=message.text)
            await state.set_state(RestaurantReview.visit_date)
            await message.answer(
                "Введите дату, когда вы были у нас в ресторане\nПример ввода: 20.05.2024"
            )
            return
    await message.answer("Неправильный формат! Попробуйте еще раз")


@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await state.set_state(RestaurantReview.food_rating)

    await message.answer("Оцените качество еды", reply_markup=main_kb())


@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    if message.text not in ["1", "2", "3", "4", "5"]:
        await message.answer("Пожалуйста, введите оценку от 1 до 5.")
    else:
        await state.update_data(food_rating=message.text)
        await state.set_state(RestaurantReview.cleanliness_rating)
        await message.answer(
            "Оцените чистоту нашего заведения", reply_markup=cleanliness_keyboard()
        )


@review_router.callback_query(
    RestaurantReview.cleanliness_rating,
    F.data.in_(["Очень чисто", "Средне чисто", "Грязно"]),
)
async def process_cleanliness_rating(callback: CallbackQuery, state: FSMContext):
    await state.update_data(cleanliness_rating=callback.data)
    await state.set_state(RestaurantReview.extra_comments)
    await callback.message.answer("Напишите комментарий нашему ресторану")
    await callback.answer()


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    await state.set_state(RestaurantReview.total_rating)
    await message.answer("Дайте общую оценку нашему ресторану", reply_markup=main_kb())


@review_router.message(RestaurantReview.total_rating)
async def process_total_rating(message: types.Message, state: FSMContext):
    await state.update_data(total_rating=message.text)
    await message.answer(
        "Ваши отзыв был принят. Спасибо!", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.clear()
