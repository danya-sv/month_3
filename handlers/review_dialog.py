from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot_config import reviewed_users

review_router = Router()


class RestaurantReview(StatesGroup):
    name = State()
    phone_number = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()


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
    if id_user in reviewed_users:
        await callback.message.answer("Вы уже оставляли отзыв!")
        await callback.answer()
        await state.clear()
    else:
        reviewed_users.add(id_user)
        await callback.answer()  # чтобы кнопка не мигала
        await state.set_state(RestaurantReview.name)
        await callback.message.answer("Напишите ваше имя")


@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(RestaurantReview.phone_number)
    await message.answer("Напишите ваш номер телефона")


@review_router.message(RestaurantReview.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(RestaurantReview.visit_date)
    await message.answer(
        "Введите дату, когда вы были у нас в ресторане\nПример ввода: 20.05.2024"
    )


@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await state.set_state(RestaurantReview.food_rating)
    food_kb = types.ReplyKeyboardMarkup(
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
    await message.answer("Оцените качество еды", reply_markup=food_kb)


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
    user_data = await state.get_data()

    review_text = (
        f"Спасибо, что уделили нам время!\n"
        f"Имя: {user_data['name']}\n"
        f"Телефон:  {user_data['phone_number']}\n"
        f"Дата визита:  {user_data['visit_date']}\n"
        f"Оценка еды:  {user_data['food_rating']}\n"
        f"Оценка чистоты:  {user_data['cleanliness_rating']}\n"
        f"Комментарий:  {user_data['extra_comments']}"
    )

    await message.answer(review_text)
    await state.clear()
