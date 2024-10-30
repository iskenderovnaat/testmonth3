from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from bot_config import database

diologs_router = Router()
list_of_homeworks = []


class FINITE_STATE_MACHINE(StatesGroup):
    name = State()
    groupe = State()
    nums_hws = State()
    link_to_github = State()


@diologs_router.callback_query(F.data == "add.homework")
async def review_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FINITE_STATE_MACHINE.name)
    await callback.message.answer(" Как вас зовут?:")
    await callback.answer()


@diologs_router.message(FINITE_STATE_MACHINE.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(FINITE_STATE_MACHINE.groupe)
    await message.answer("Введите название вашей группы")


@diologs_router.message(FINITE_STATE_MACHINE.groupe)
async def groupe_handler(message: types.Message, state: FSMContext):
    await state.update_data(groupe=message.text)
    await state.set_state(FINITE_STATE_MACHINE.nums_hws)

    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="1"),
             types.KeyboardButton(text="2"),
             types.KeyboardButton(text="3"),
             types.KeyboardButton(text="4"),
             types.KeyboardButton(text="5"),
             types.KeyboardButton(text="6"),
             types.KeyboardButton(text="7"),
             types.KeyboardButton(text="8")]
        ],
        resize_keyboard=True
    )

    await message.answer("Введите номер вашего домашнего задания", reply_markup=kb)


@diologs_router.message(FINITE_STATE_MACHINE.nums_hws)
async def nums_hws_handler(message: types.Message, state: FSMContext):
    num = int(message.text)
    if num > 8 or num < 1:
        await message.answer("Номер группы должен быть от 1 до 8")
        return

    await state.update_data(nums_hws=message.text)
    await state.set_state(FINITE_STATE_MACHINE.link_to_github)
    await message.answer(" ПОЖАЛУЙСТА,вставьте ссылку на GitHub репозиторий")


@diologs_router.message(FINITE_STATE_MACHINE.link_to_github)
async def link_to_github_handler(message: types.Message, state: FSMContext):
    if not message.text.startswith("https://github.com/"):
        await message.answer("Ссылка должна начинаться с https://github.com/  !!!!!")
        return

    await state.update_data(link_to_github=message.text)
    data = await state.get_data()
    list_of_homeworks.append(data)
    print(list_of_homeworks)

    database.execute(
        query="INSERT INTO homeworks (name, groupe, nums_hws, link_to_github)"
              " VALUES (?, ?, ?, ?)",
        params=(
            data['name'],
            data['groupe'],
            data['nums_hws'],
            data['link_to_github'])
    )

    await state.clear()
    await message.answer("Домашнее задание  успешно добавлено!")