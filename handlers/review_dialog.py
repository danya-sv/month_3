from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

review_router = Router()

reviewed_users = set()


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
            [types.InlineKeyboardButton(text="Очень чисто", callback_data="Очень чисто")],
            [types.InlineKeyboardButton(text="Средне чисто", callback_data="Средне чисто")],
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
    await message.answer("Введите дату, когда вы были у нас в ресторане\nПример ввода: 20.05.2024")


@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await state.set_state(RestaurantReview.food_rating)
    food_kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Отлично",
                    callback_data="Отлично"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Удовлетворительно",
                    callback_data="Удовлетворительно"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Плохо",
                    callback_data="Плохо"
                )
            ]
        ]
    )
    await message.answer("Оцените качество еды", reply_markup=food_kb)


@review_router.callback_query(F.data == "Отлично")
async def exe(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(food_rating="Отлично")
    await state.set_state(RestaurantReview.cleanliness_rating)
    await callback.message.answer("Оцените чистоту нашего заведения", reply_markup=cleanliness_keyboard())
    await callback.answer()


@review_router.callback_query(F.data == "Удовлетворительно")
async def mid(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(food_rating="Удовлетворительно")
    await state.set_state(RestaurantReview.cleanliness_rating)
    await callback.message.answer("Оцените чистоту нашего заведения", reply_markup=cleanliness_keyboard())
    await callback.answer()


@review_router.callback_query(F.data == "Плохо")
async def bad(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(food_rating="Плохо")
    await state.set_state(RestaurantReview.cleanliness_rating)
    await callback.message.answer("Оцените чистоту нашего заведения", reply_markup=cleanliness_keyboard())
    await callback.answer()


@review_router.message(RestaurantReview.food_rating)
async def process_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    await state.set_state(RestaurantReview.cleanliness_rating)
    await message.answer("Оцените чистоту нашего заведения")


@review_router.callback_query(F.data == "Очень чисто")
async def great(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(cleanliness_rating="Очень чисто")
    await state.set_state(RestaurantReview.extra_comments)
    await callback.message.answer("Напишите комментарий нашему ресторану")
    await callback.answer()


@review_router.callback_query(F.data == "Средне чисто")
async def middle(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(cleanliness_rating="Средне чисто")
    await state.set_state(RestaurantReview.extra_comments)
    await callback.message.answer("Напишите комментарий нашему ресторану")
    await callback.answer()


@review_router.callback_query(F.data == "Грязно")
async def baad(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(cleanliness_rating="Грязно")
    await state.set_state(RestaurantReview.extra_comments)
    await callback.message.answer("Напишите комментарий нашему ресторану")
    await callback.answer()


@review_router.message(RestaurantReview.cleanliness_rating)
async def process_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(cleanliness_rating=message.text)
    await state.set_state(RestaurantReview.extra_comments)
    await message.answer("Напишите комментарий нашему ресторану")


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    user_data = await state.get_data()

    review_text = (
        f"Спасибо, что уделили нам время!\n"
        f"Имя: {user_data['name']}\n"
        f"Телефон: {user_data['phone_number']}\n"
        f"Дата визита: {user_data['visit_date']}\n"
        f"Оценка еды: {user_data['food_rating']}\n"
        f"Оценка чистоты: {user_data['cleanliness_rating']}\n"
        f"Комментарий: {user_data['extra_comments']}"
    )

    await message.answer(review_text)
    await state.clear()
