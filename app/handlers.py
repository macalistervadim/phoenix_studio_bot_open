import aiogram

import app.database.models
import app.database.requests
import app.keyboards
import app.messages

router = aiogram.Router()


@router.message(aiogram.filters.CommandStart())
async def cmd_start(message: aiogram.types.Message):
    await message.answer(app.messages.START_MESSAGE, reply_markup=app.keyboards.MAIN)


@router.message(aiogram.F.text == "📪 Контакты")
async def cmd_contacts(message: aiogram.types.Message):
    await message.answer(app.messages.CONTACTS_MESSAGE, reply_markup=app.keyboards.MAIN)
