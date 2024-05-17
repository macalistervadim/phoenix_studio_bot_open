import datetime
import os
import typing


import aiogram

import app.database.requests
import app.keyboards
import app.messages


class ChechSubUser(aiogram.BaseMiddleware):
    """
    Проверка подписки на ТГ канал
    """

    def __init__(self, bot):
        self.bot = bot

    async def __call__(
        self,
        handler: typing.Callable[
            [aiogram.types.Message, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any],
        ],
        event: aiogram.types.Message,
        data: typing.Dict[str, typing.Any],
    ) -> typing.Any:
        user_channel_status = await self.bot.get_chat_member(
            chat_id=os.getenv("TG_CHANNEL_ID", "-1002064780409"),
            user_id=data["event_from_user"].id,
        )
        if (
            user_channel_status.status != "left"
            or data["event_update"].message.text == "/start"
        ):
            return await handler(event, data)

        await event.answer(
            app.messages.SUBSCRIPTION_MESSAGE,
            reply_markup=app.keyboards.SUBSCRIPTION,
            parse_mode=aiogram.enums.ParseMode.HTML,
        )


class RegistrationNewUser(aiogram.BaseMiddleware):
    """
    Мидлварь для создания нового юзера в БД
    """

    async def __call__(
        self,
        handler: typing.Callable[
            [aiogram.types.Message, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any],
        ],
        event: aiogram.types.Message,
        data: typing.Dict[str, typing.Any],
    ) -> typing.Any:

        async with app.database.models.async_session() as session:
            await app.database.requests.add_user(
                session,
                tg_id=data["event_from_user"].id,
            )

        return await handler(event, data)


class CancelCommand(aiogram.BaseMiddleware):
    """
    Мидлварь для кнопки отмены (сброс стейта)
    """

    async def __call__(
        self,
        handler: typing.Callable[
            [aiogram.types.Message, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any],
        ],
        event: aiogram.types.Message,
        data: typing.Dict[str, typing.Any],
    ) -> typing.Any:

        if data["event_update"].message.text == "Отменить":
            await data["state"].clear()
            await event.answer("💤 Выполнение команды отменено")
            return

        return await handler(event, data)


class CheckWaitingOrder(aiogram.BaseMiddleware):
    """
    Проверка нахождения пользователя в состоянии ожидания заказа
    """

    async def __call__(
        self,
        handler: typing.Callable[
            [aiogram.types.Message, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any],
        ],
        event: aiogram.types.Message,
        data: typing.Dict[str, typing.Any],
    ) -> typing.Any:

        async with app.database.models.async_session():
            user = await app.database.requests.get_user(
                tg_id=data["event_from_user"].id,
            )

            if (
                data["event_update"].message.text == "Отменить заказ"
                or user.waiting_order is False
            ):
                return await handler(event, data)

            elif user.waiting_order is True:
                await event.answer(
                    app.messages.WAITING_ORDER_MESSAGE,
                    parse_mode=aiogram.enums.ParseMode.HTML,
                )


class CheckTime(aiogram.BaseMiddleware):
    """
    Мидлварь для проверки часов работы студии
    """

    async def __call__(
        self,
        handler: typing.Callable[
            [aiogram.types.Message, typing.Dict[str, typing.Any]],
            typing.Awaitable[typing.Any],
        ],
        event: aiogram.types.Message,
        data: typing.Dict[str, typing.Any],
    ) -> typing.Any:

        start_time = datetime.time(10, 0)
        end_time = datetime.time(21, 0)

        formatted_start_time = start_time.strftime("%H:%M")
        formatted_end_time = end_time.strftime("%H:%M")

        if start_time <= datetime.datetime.now().time() <= end_time:
            return await handler(event, data)
        return event.answer(
            "Упс!\n\n"
            "🙈 К сожалению, время работы нашего бота вышло.\n"
            f"Время работы бота: с {formatted_start_time} до {formatted_end_time} часов",
        )
