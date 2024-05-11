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
