import os
import asyncio
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message

TOKEN = os.getenv("TOKEN")  # Токен бота
ADMIN_ID = int(os.getenv("ADMIN_ID"))  # Твой Telegram ID (число)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранение заблокированных пользователей
banned_users = set()

# Отслеживание количества сообщений (для авто-блокировки)
user_spam_count = {}
user_last_message_time = {}

# Хранение сообщений пользователей (для ответа)
user_messages = {}
user_notified = set()

@dp.message()
async def handle_messages(message: Message):
    """Пересылает сообщения админу и позволяет отвечать обратно"""
    user_id = message.from_user.id

    # Если пользователь в бане, игнорируем его сообщения
    if user_id in banned_users:
        return

    # Антиспам-система
    current_time = time.time()
    last_time = user_last_message_time.get(user_id, 0)

    if user_id in user_spam_count:
        if current_time - last_time < 3:  # Если сообщение отправлено менее чем через 3 сек
            user_spam_count[user_id] += 1
        else:
            user_spam_count[user_id] = 1
    else:
        user_spam_count[user_id] = 1

    user_last_message_time[user_id] = current_time

    if user_spam_count[user_id] > 5:
        banned_users.add(user_id)
        await message.answer("Вы были заблокированы за спам.")
        await bot.send_message(ADMIN_ID, f"❌ Пользователь {user_id} заблокирован за спам!")
        return

    # Если пишет обычный пользователь
    if user_id != ADMIN_ID:
        user_messages[message.message_id] = user_id
        text = f"Сообщение от {message.from_user.full_name} (@{message.from_user.username}):\n\n{message.text}"
        sent_msg = await bot.send_message(ADMIN_ID, text)
        user_messages[sent_msg.message_id] = user_id

        if user_id not in user_notified:
            await message.answer("Привет, это Ozzi Hacking Bot! Пришли куки жертвы и мы скоро дадим его данные аккаунт тебе :)")
            user_notified.add(user_id)

    else:  # Админ отвечает
        if message.reply_to_message and message.reply_to_message.message_id in user_messages:
            target_user = user_messages[message.reply_to_message.message_id]
            await bot.send_message(target_user, f"{message.text}")

@dp.message(commands=['ban'])
async def ban_user(message: Message):
    """Команда для блокировки пользователя (только для админа)"""
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])
        if user_id in banned_users:
            await message.answer(f"⚠️ Пользователь {user_id} уже в бане.")
        else:
            banned_users.add(user_id)
            await message.answer(f"✅ Пользователь {user_id} заблокирован.")
            await bot.send_message(user_id, "Вы были заблокированы администратором.")
    except (IndexError, ValueError):
        await message.answer("⚠️ Используйте команду так: `/ban user_id`")

@dp.message(commands=['unban'])
async def unban_user(message: Message):
    """Разблокировка пользователя (только для админа)"""
    if message.from_user.id != ADMIN_ID:
        return

    try:
        user_id = int(message.text.split()[1])
        if user_id in banned_users:
            banned_users.remove(user_id)
            await message.answer(f"✅ Пользователь {user_id} разблокирован.")
        else:
            await message.answer(f"⚠️ Пользователь {user_id} не был в бане.")
    except (IndexError, ValueError):
        await message.answer("⚠️ Используйте команду так: `/unban user_id`")

async def main():
    """Запуск бота"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
