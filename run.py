import asyncio
import logging
import os
import sys

import aiogram
import dotenv

import app.database.models
import app.handlers


dotenv.load_dotenv()


async def main():
    await app.database.models.async_main()

    bot = aiogram.Bot(token=os.getenv("BOT_TOKEN", default="not_secret"))
    dp = aiogram.Dispatcher()

    dp.include_router(app.handlers.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
