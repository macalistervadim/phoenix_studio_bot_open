import aiogram

import app.database.models
import app.database.requests


router = aiogram.Router()


@router.message(aiogram.filters.CommandStart())
async def cmd_start(message: aiogram.types.Message):
    async with app.database.models.async_session() as session:
        await app.database.requests.add_user(session, tg_id=message.from_user.id)

    await message.answer("Дадова!")
