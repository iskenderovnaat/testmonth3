import asyncio
import logging

from handlers.start import start_router
from handlers.hw import diologs_router
from aiogram import Bot

from bot_config import bot, dp, database


async def start_db():
    print("База данных созданна")
    database.create_table()


async def main():
    dp.include_router(start_router)
    dp.include_router(diologs_router)

    dp.startup.register(start_db)

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())