import aiogram
import aiogram.utils.keyboard


MAIN = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [aiogram.types.KeyboardButton(text="📚 Каталог")],
        [aiogram.types.KeyboardButton(text="📪 Контакты")],
        [aiogram.types.KeyboardButton(text="📨 Тех. поддержка")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)

SUBSCRIPTION = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [aiogram.types.KeyboardButton(text="✅ Подписался")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)

CANCEL_OR_BACK = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [aiogram.types.KeyboardButton(text="Отменить")],
        [aiogram.types.KeyboardButton(text="Назад")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)
