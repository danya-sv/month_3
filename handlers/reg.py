from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery


from bot_config import reg_account, reg_users, registered_users, database

reg_router = Router()


class Reg(StatesGroup):
    name = State()
    age = State()
    phone_number = State()
    city = State()


@reg_router.callback_query(F.data == "reg")
async def start_reg(callback_query: CallbackQuery, state: FSMContext):
    user = callback_query.from_user.id
    if user in reg_account:
        await callback_query.message.answer("Вы уже зарегистрированы!!!")
        await callback_query.answer()
        await state.clear()
    else:
        reg_account.add(user)
        await state.set_state(Reg.name)
        await callback_query.answer()
        await callback_query.message.answer("Введите своё имя")


@reg_router.message(Reg.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.age)
    await message.answer("Введите свой возраст")


@reg_router.message(Reg.age)
async def process_age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(Reg.phone_number)
    await message.answer("Введите свой номер телефона")


@reg_router.message(Reg.phone_number)
async def process_phone_number(message: types.Message, state: FSMContext):
    code_num = ["+996", "+7", "+33", "+49", "+39", "+44", "+1"]
    for code in code_num:
        if message.text.startswith(code):
            await state.update_data(phone_number=message.text)
            await state.set_state(Reg.city)
            await message.answer("Введите свой город")
            return
    await message.answer("Неправильный формат! Попробуйте еще раз")


@reg_router.message(Reg.city)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    reg_data = await state.get_data()

    registered_users[message.from_user.id] = reg_data["name"]
    reg_users[message.from_user.id] = reg_data["phone_number"]

    await message.answer(
        f"Вы успешно зарегистрировались!\n"
        f"Ваши данные:\n"
        f"Имя: {reg_data['name']}\n"
        f"Возраст: {reg_data['age']}\n"
        f"Номер телефона: {reg_data['phone_number']}\n"
        f"Город: {reg_data['city']}"
    )
    dta = await state.get_data()
    database.execute(
        query="""
          INSERT INTO reg_users (name, age, phone_number, city)
          VALUES (?,?,?,?)      
        """,
        params=(dta["name"], dta["age"], dta["phone_number"], dta["city"])
    )
    await state.clear()