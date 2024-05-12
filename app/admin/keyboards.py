import aiogram
import aiogram.utils.keyboard


ADMIN_COMMANDS = aiogram.types.ReplyKeyboardMarkup(
    keyboard=[
        [
            aiogram.types.KeyboardButton(text="Создание товара/услуги"),
            aiogram.types.KeyboardButton(text="Редактирование товара/услуги"),
        ],
        [
            aiogram.types.KeyboardButton(text="Создание промокода"),
            aiogram.types.KeyboardButton(text="Редактирование промокода"),
        ],
    ],
    row_width=2,
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню",
)
