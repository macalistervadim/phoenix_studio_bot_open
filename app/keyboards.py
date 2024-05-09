import aiogram


MAIN = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [aiogram.types.KeyboardButton(text="📚 Каталог")],
        [aiogram.types.KeyboardButton(text="📪 Контакты")],
        [aiogram.types.KeyboardButton(text="📨 Тех. поддержка")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)
