import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router
from config import API_TOKEN

async def on_start():
    bot = Bot(token=API_TOKEN)  # Создаем объект бота
    storage = MemoryStorage()  # Используем память для хранения состояний
    dp = Dispatcher(storage=storage)  # Передаем хранилище в диспетчер

    dp.include_router(router)  # Подключаем маршрутизатор
    await dp.start_polling(bot)  # Запускаем бота на обработку сообщений

if __name__ == "__main__":
    asyncio.run(on_start())
