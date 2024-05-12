import os

import aiogram

import app.admin.filters
import app.admin.keyboards
import app.admin.states
import app.database.models
import app.database.requests
import app.keyboards


router = aiogram.Router()


@router.message(
    app.admin.filters.IsAdmin(os.getenv("ADMIN_ID", "null_admins")),
    aiogram.F.text == "/admin",
)
async def cmd_admin(message: aiogram.types.Message):
    await message.answer(
        "🔰 Открываю админку...",
        reply_markup=app.admin.keyboards.ADMIN_COMMANDS,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )


@router.message(
    app.admin.filters.IsAdmin(os.getenv("ADMIN_ID", "null_admins")),
    aiogram.F.text == "Создание товара/услуги",
)
async def cmd_create_item(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await message.answer(
        "❗️ Начинаем процесс создания нового товара/услуги...\n"
        "Введите название нового товара:",
        reply_markup=app.keyboards.CANCEL_OR_BACK,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )

    await state.set_state(app.admin.states.CreateItem.title)


@router.message(app.admin.states.CreateItem.title)
async def create_item_title(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(title=message.text.lower())

    await message.answer(
        "❗️ Теперь необходимо ввести описание товара/услуги (макс. 250 символов)",
    )

    await state.set_state(app.admin.states.CreateItem.description)


@router.message(app.admin.states.CreateItem.description)
async def create_item_description(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(description=message.text.lower())

    await message.answer("❗️ Прикрепите одно изображение к товару/услуге")

    await state.set_state(app.admin.states.CreateItem.image)


@router.message(aiogram.F.photo, app.admin.states.CreateItem.image)
async def create_item_image(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(image=message.photo[-2])

    await message.answer("❗️ Укажите цену за товар/услугу (в руб.)")

    await state.set_state(app.admin.states.CreateItem.price)


@router.message(app.admin.states.CreateItem.price)
async def create_item_price(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(price=message.text.lower())

    await message.answer("❗️ Укажите примерное время выполнения в днях")

    await state.set_state(app.admin.states.CreateItem.deadline)


@router.message(app.admin.states.CreateItem.deadline)
async def create_item_deadline(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(deadline=message.text.lower())
    data = await state.get_data()

    try:
        async with app.database.models.async_session() as session:
            await app.database.requests.add_item(session, data)

        response_text = (
            f"✅ <b>Отлично, товар создан:</b>\n\n"
            f"Название: {data.get('title')}\n\n"
            f"Описание: {data.get('description')}\n\n"
            f"Цена: {data.get('price')} руб.\n"
            f"Дедлайн: {data.get('deadline')} дней"
        )
        await message.answer(response_text, parse_mode=aiogram.enums.ParseMode.HTML)
        await message.answer_photo(data.get("image").file_id)

        await state.clear()
    except ValueError as e:
        await message.answer(
            "🚫 Упс... кажется вы допустили ошибку при создании товара/услуги\n"
            f"Код ошибки: {e.args[0]}\n\n"
            "Вы можете попробовать создать товар/услугу заново",
            parse_mode=aiogram.enums.ParseMode.HTML,
        )
