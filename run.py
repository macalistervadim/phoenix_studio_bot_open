import asyncio
import logging
import os
import sys

import aiogram
import dotenv

import app.admin.handlers
import app.database.models
import app.handlers
import app.middlewares


dotenv.load_dotenv()


async def main():
    await app.database.models.async_main()

    bot = aiogram.Bot(token=os.getenv("BOT_TOKEN", default="not_secret"))
    dp = aiogram.Dispatcher()

    dp.include_router(app.handlers.router)
    dp.include_router(app.admin.handlers.router)  # Роутер для админ-команд

    dp.message.middleware(app.middlewares.RegistrationNewUser())
    dp.message.middleware(app.middlewares.ChechSubUser(bot))
    dp.message.middleware(app.middlewares.CancelCommand())
    dp.message.middleware(app.middlewares.CheckTime())

    await bot(
        aiogram.methods.DeleteWebhook(drop_pending_updates=True),
    )  # Перед запуском скипаем старые сообщения в боте
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
