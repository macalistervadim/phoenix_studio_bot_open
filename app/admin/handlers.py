import os

import aiogram

import app.admin.filters
import app.admin.keyboards
import app.admin.states
import app.database.admin.requests
import app.database.models
import app.database.requests
import app.keyboards
import app.messages


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
    aiogram.F.text == "Удаление промокода",
)
async def cmd_delete_pcode(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await message.answer(
        "❗️ Начинаем процесс удаления промокода...\n\n"
        "Укажите название промокода, который хотите удалить:",
        reply_markup=app.keyboards.CANCEL_OR_BACK,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )

    await state.set_state(app.admin.states.DeletePocde.name)


@router.message(app.admin.states.DeletePocde.name)
async def delete_pcode_name(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(name=message.text.lower())

    pcode = await app.database.admin.requests.get_pcode(message.text.lower())
    await state.update_data(pcode=pcode)

    if pcode:
        await message.answer(
            "❗️ Вы уверены, что выбрали верный промокод?\n\n"
            f"{pcode.name.title()}\n"
            f"Скидка: {pcode.discount}%\n"
            f"Активаций: {pcode.activations}",
            reply_markup=app.admin.keyboards.CHOICE_EDIT_ITEM,
        )

    elif pcode is None:
        await message.answer(
            app.messages.FAILED_MESSAGE,
            parse_mode=aiogram.enums.ParseMode.HTML,
        )

    await state.set_state(app.admin.states.DeletePocde.choice)


@router.message(app.admin.states.DeletePocde.choice)
async def delete_pcode_choice(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    data = await state.get_data()

    if message.text == "Верно":
        async with app.database.models.async_session() as session:
            await app.database.admin.requests.delete_pcode(
                session,
                data.get("pcode").name,
            )
        await message.answer(
            f"✅ Промокод - {data.get('name')} успешно удален из базы данных",
        )

    elif message.text == "Неверно":
        await message.answer("✅ Понял... Отменяем процесс удаления промокода")

    await state.clear()


@router.message(
    app.admin.filters.IsAdmin(os.getenv("ADMIN_ID", "null_admins")),
    aiogram.F.text == "Создание промокода",
)
async def cmd_create_pcode(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await message.answer(
        "❗️ Начинаем процесс создания нового промокода...\n\n"
        "Укажите название промокода:",
        reply_markup=app.keyboards.CANCEL_OR_BACK,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )

    await state.set_state(app.admin.states.CreatePcode.name)


@router.message(app.admin.states.CreatePcode.name)
async def create_pcode_name(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(name=message.text.lower())

    await message.answer(
        "❗️ Теперь необходимо указать процент скидки (укажите просто цифру, например: 25):",
    )

    await state.set_state(app.admin.states.CreatePcode.discount)


@router.message(app.admin.states.CreatePcode.discount)
async def create_pcode_discount(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(discount=message.text.lower())

    await message.answer("❗️ Укажите число активаций (просто цифру):")

    await state.set_state(app.admin.states.CreatePcode.activations)


@router.message(app.admin.states.CreatePcode.activations)
async def create_pcode_activations(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(activations=message.text.lower())
    author = await app.database.requests.get_user(message.from_user.id)
    await state.update_data(author=author.id)
    data = await state.get_data()

    async with app.database.models.async_session() as session:
        await app.database.admin.requests.add_pcode(session, data)

    await message.answer(
        f"✅ Вы успешно создали промокод: {data.get('name')}\n"
        f"Число активаций: {data.get('activations')}\n"
        f"Скидка: {data.get('discount')}%",
    )

    await state.clear()


@router.message(
    app.admin.filters.IsAdmin(os.getenv("ADMIN_ID", "null_admins")),
    aiogram.F.text == "Удаление товара/услуги",
)
async def cmd_delete_item(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await message.answer(
        "❗️ Начинаем процесс удаления товара/услуги...\n\n"
        "Укажите название товара, который хотите удалить:",
        reply_markup=app.keyboards.CANCEL_OR_BACK,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )

    await state.set_state(app.admin.states.DeleteItem.item)


@router.message(app.admin.states.DeleteItem.item)
async def delete_item_item(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(item=message.text.lower())

    object = await app.database.admin.requests.get_editable_item(message.text.lower())
    await state.update_data(object_db=object)

    if object:
        await message.answer(
            "❗️ Вы уверены, что выбрали верный товар/услугу?\n\n"
            f"{object.title.title()}\n"
            f"{object.description}\n\n"
            f"Цена: {object.price} руб.\n"
            f"Сроки выполнения: {object.deadline} дней",
            reply_markup=app.admin.keyboards.CHOICE_EDIT_ITEM,
        )

    elif object is None:
        await message.answer(
            app.messages.FAILED_MESSAGE,
            parse_mode=aiogram.enums.ParseMode.HTML,
        )

    await state.set_state(app.admin.states.DeleteItem.choice)


@router.message(app.admin.states.DeleteItem.choice)
async def delete_item_choice(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    data = await state.get_data()

    if message.text == "Верно":
        async with app.database.models.async_session() as session:
            await app.database.admin.requests.delete_item(
                session,
                data.get("object_db").title,
            )
        await message.answer(
            f"✅ Товар/услуга - {data.get('item')} успешно удален из базы данных",
        )

    elif message.text == "Неверно":
        await message.answer("✅ Понял... Отменяем процесс удаления товара/услуги")

    await state.clear()


@router.message(
    app.admin.filters.IsAdmin(os.getenv("ADMIN_ID", "null_admins")),
    aiogram.F.text == "Редактирование товара/услуги",
)
async def cmd_edit_item(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await message.answer(
        "❗️ Начинаем процесс редактирования товара/услуги...\n\n"
        "Введите название товара/услуги, которую бы вы хотели отредактировать "
        "(ВНИМАНИЕ: Вводите точное название товара, иначе в боте возникнет ошибка):",
        reply_markup=app.keyboards.CANCEL_OR_BACK,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )

    await state.set_state(app.admin.states.EditItem.item)


@router.message(app.admin.states.EditItem.item)
async def edit_item_itemobject(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(object=message.text.lower())

    object = await app.database.admin.requests.get_editable_item(message.text.lower())
    await state.update_data(object_db=object)

    if object:
        await message.answer(
            "✅ Отправляю выбранный вами на редакцию товар...",
        )
        await message.answer_photo(object.image)
        await message.answer(
            f"<b>{object.title.title()}</b>\n\n"
            f"{object.description}\n\n"
            f"Цена: {object.price} руб.\n"
            f"Срок выполнения: {object.deadline} дней",
            parse_mode=aiogram.enums.ParseMode.HTML,
        )
        await message.answer(
            "❗️ Пожалуйста, убедитесь что вы выбрали <b>нужный товар</b> и нажмите соответствующую кнопку...",
            parse_mode=aiogram.enums.ParseMode.HTML,
            reply_markup=app.admin.keyboards.CHOICE_EDIT_ITEM,
        )

        await state.set_state(app.admin.states.EditItem.choice)

    elif object is None:
        await message.answer(
            app.messages.FAILED_MESSAGE,
            parse_mode=aiogram.enums.ParseMode.HTML,
        )

        await state.clear()


@router.message(app.admin.states.EditItem.choice)
async def edit_item_choice(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    if message.text == "Верно":
        await message.answer(
            "Отлично, тогда продолжаем редактирование. Что будем редактировать?\n"
            "<b>1) Название</b>\n"
            "<b>2) Описание</b>\n"
            "<b>3) Цена</b>\n"
            "<b>4) Сроки выполнения</b>\n"
            "<b>5) Фотографию</b>\n\n"
            "❗️ Вам необходимо прислать мне <b>ЦИФРУ</b> обозначающую значение, которое вы хотите отредактировать",
            parse_mode=aiogram.enums.ParseMode.HTML,
            reply_markup=app.keyboards.CANCEL_OR_BACK,
        )

        await state.set_state(app.admin.states.EditItem.editable_object)
    else:
        await message.answer("👋 Понял, в таком случае отменяю редактирование...")

        await state.clear()


@router.message(app.admin.states.EditItem.editable_object)
async def edit_item_editable_object(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(editable_object=message.text.lower())
    data = await state.get_data()
    object = data.get("object_db")

    if message.text == "1":
        await message.answer(
            f"✅ Ваш выбранный элемент - 1) Название\n"
            f"Название: {object.title}\n\n"
            "❗️ Теперь введите новое название для товара/услуги (регистр не имеет значение)",
            reply_markup=app.keyboards.CANCEL_OR_BACK,
        )

    if message.text == "2":
        await message.answer(
            f"✅ Ваш выбранный элемент - 2) Описание\n"
            f"Описание: {object.description}\n\n"
            "❗️ Теперь введите новое описание для товара/услуги <b>(регистр не имеет значение)</b>",
            parse_mode=aiogram.enums.ParseMode.HTML,
            reply_markup=app.keyboards.CANCEL_OR_BACK,
        )

    if message.text == "3":
        await message.answer(
            f"✅ Ваш выбранный элемент - 3) Цена\n"
            f"Цена: {object.price} руб.\n\n"
            "❗️ Теперь введите новую цену для товара/услуги <b>(в рублях)</b>",
            parse_mode=aiogram.enums.ParseMode.HTML,
            reply_markup=app.keyboards.CANCEL_OR_BACK,
        )

    if message.text == "4":
        await message.answer(
            f"✅ Ваш выбранный элемент - 4) Сроки выполнения\n"
            f"Сроки выполнения: {object.deadline} дней\n\n"
            "❗️ Теперь введите новые сроки выполнения для товара/услуги <b>(кол-во дней)</b>",
            parse_mode=aiogram.enums.ParseMode.HTML,
            reply_markup=app.keyboards.CANCEL_OR_BACK,
        )

    if message.text == "5":
        await message.answer_photo(object.image)
        await message.answer(
            "✅ Ваш выбранный элемент - 5) Фотография\n\n"
            "❗️ Теперь отправьте новую фотографию для товара",
            parse_mode=aiogram.enums.ParseMode.HTML,
            reply_markup=app.keyboards.CANCEL_OR_BACK,
        )

    await state.set_state(app.admin.states.EditItem.edit_item)


@router.message(app.admin.states.EditItem.edit_item)
async def edit_item_edit_item(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    data = await state.get_data()
    edit_item = message.text.lower() if message.text else None

    if data.get("editable_object") == "5":
        edit_item = message.photo[-2] if message.photo else None

    if edit_item is None:
        await state.clear()
        return

    async with app.database.models.async_session() as session:
        if data.get("editable_object") == "1":
            await app.database.admin.requests.updata_item_title(
                session,
                data.get("object_db").title,
                edit_item,
            )
            edit_object = "Название"
        elif data.get("editable_object") == "2":
            await app.database.admin.requests.updata_item_description(
                session,
                data.get("object_db").description,
                edit_item,
            )
            edit_object = "Описание"
        elif data.get("editable_object") == "3":
            await app.database.admin.requests.updata_item_price(
                session,
                data.get("object_db").price,
                edit_item,
            )
            edit_object = "Цена"
        elif data.get("editable_object") == "4":
            await app.database.admin.requests.updata_item_deadline(
                session,
                data.get("object_db").deadline,
                edit_item,
            )
            edit_object = "Сроки выполнения"
        elif data.get("editable_object") == "5":
            await app.database.admin.requests.updata_item_image(
                session,
                data.get("object_db").image,
                edit_item.file_id,
            )
            edit_object = "Фотография"

    await message.answer(
        f"✅ Вы успешно отредактировали товар - {data.get('object')}\n\n"
        f"Редактируемый объект - {data.get('editable_object')}) {edit_object}\n"
        f"Отредактировали на - {edit_item if isinstance(edit_item, str) else ''}\n",
    )

    if isinstance(edit_item, aiogram.types.PhotoSize):
        await message.answer_photo(edit_item.file_id)

    await state.clear()


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
