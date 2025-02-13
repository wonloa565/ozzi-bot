import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message

TOKEN = os.getenv("8064407397:AAFRHKy3qgElrQT8XrdU9ZkS1s5tFwPyaBg")  # Токен бота (Railway переменная)
ADMIN_ID = os.getenv("7395692166")  # Твой Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Обрабатываем входящие сообщения
@dp.message_handler()
async def forward_to_admin(message: Message):
    """Пересылает сообщение админу и отправляет автоответ пользователю"""
    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"Сообщение от {message.from_user.full_name} (@{message.from_user.username}):\n\n{message.text}")
    await message.answer("Спасибо! Ваше сообщение получено, мы скоро ответим.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
