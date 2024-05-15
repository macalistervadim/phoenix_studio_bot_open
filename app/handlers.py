import aiogram

import app.database.models
import app.database.requests
import app.keyboards
import app.messages
import app.states as st


router = aiogram.Router()


@router.message(aiogram.filters.CommandStart())
async def cmd_start(message: aiogram.types.Message):
    await message.answer(
        app.messages.START_MESSAGE,
        reply_markup=app.keyboards.MAIN,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )


@router.message(aiogram.F.text == "📪 Контакты")
async def cmd_contacts(message: aiogram.types.Message):
    await message.answer(
        app.messages.CONTACTS_MESSAGE,
        reply_markup=app.keyboards.MAIN,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )


@router.message(aiogram.F.text == "💚 Вывести команды")
async def cmd_keyboard(message: aiogram.types.Message):
    await message.answer(
        "Секунду... Уже вывожу вам свои команды 💚",
        reply_markup=app.keyboards.MAIN,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )


@router.message(aiogram.F.text == "📚 Каталог")
async def cmd_catalog(message: aiogram.types.Message):
    request = await app.database.requests.get_catalog()

    if request:
        await message.answer("♻️ Секунду, уже достаю каталог и пересылаю вам...")
        for i in request:

            keyboard = aiogram.utils.keyboard.InlineKeyboardBuilder()
            keyboard.add(
                aiogram.types.InlineKeyboardButton(
                    text="Выбрать",
                    callback_data=f"product_{str(i.id)}",
                ),
            )

            await message.answer_photo(i.image)
            await message.answer(
                f"<b>{i.title.title()}</b>\n\n"
                f"{i.description}\n\n"
                f"Цена за услугу: {i.price} руб.\n"
                f"Срок выполнения: {i.deadline} дней",
                parse_mode=aiogram.enums.ParseMode.HTML,
                reply_markup=keyboard.as_markup(),
            )

    else:
        await message.answer(
            "♻️ К сожалению, каталог пуст",
            parse_mode=aiogram.enums.ParseMode.HTML,
        )


@router.callback_query(aiogram.F.data.startswith("product_"))
async def product_selected(
    callback: aiogram.types.CallbackQuery,
    state: aiogram.fsm.context.FSMContext,
):
    await state.update_data(item_id=callback.data[-1])

    await callback.message.answer(
        "♻️ Начинаем процесс оформления заказа...\n"
        f"Ваш выбранный товар - №{callback.data[-1]}\n\n"
        "Пожалуйста, укажите ваше Техническое задание к заказу (если это товар - напишите 0)",
    )

    await state.set_state(st.CreateOrder.description_order)


@router.message(st.CreateOrder.description_order)
async def order_create_description(
    message: aiogram.types.Message,
    state: aiogram.fsm.context.FSMContext,
):
    async with app.database.models.async_session() as session:
        user = await app.database.requests.get_user(
            message.from_user.id,
        )
        await state.update_data(user=user.id)

        await app.database.requests.update_user(
            session,
            tg_id=message.from_user.id,
        )

        data = await state.get_data()
        await app.database.requests.add_order(
            session,
            data,
        )

        await message.answer(
            app.messages.SUCC_CREATE_ORDER_MESSAGE,
            parse_mode=aiogram.enums.ParseMode.HTML,
        )

        await state.clear()


@router.message(aiogram.F.text == "✅ Подписался")
async def cmd_subscription(message: aiogram.types.Message):
    await message.answer(
        app.messages.SUBSCRIPTION_SUCC_MESSAGE,
        reply_markup=app.keyboards.MAIN,
        parse_mode=aiogram.enums.ParseMode.HTML,
    )
