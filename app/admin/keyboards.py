import aiogram
import aiogram.utils.keyboard


ADMIN_COMMANDS = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [
            aiogram.types.KeyboardButton(text="Создание товара/услуги"),
            aiogram.types.KeyboardButton(text="Редактирование товара/услуги"),
            aiogram.types.KeyboardButton(text="Удаление товара/услуги"),
        ],
        [
            aiogram.types.KeyboardButton(text="Создание промокода"),
            aiogram.types.KeyboardButton(text="Редактирование промокода"),
            aiogram.types.KeyboardButton(text="Удаление промокода"),
        ],
    ],
    row_width=3,
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)

CHOICE_EDIT_ITEM = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [aiogram.types.KeyboardButton(text="Верно")],
        [aiogram.types.KeyboardButton(text="Неверно")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)
