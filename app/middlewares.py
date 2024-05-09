import typing

import aiogram

import app.database.requests


class RegistrationNewUser(aiogram.BaseMiddleware):
    # Мидльварь для создания нового юзера в БД

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
