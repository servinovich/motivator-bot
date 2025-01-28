import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command  # Импортируем фильтр для команд
from config import BOT_TOKEN
from database import get_motivation

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Создаем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функция для обработки команды /start
async def send_welcome(message: Message):
    await message.reply("Hello! I am your motivational coach. Tell me what's on your mind, and I'll help!")

# Функция для обработки входящих сообщений
from aiogram.types import Message
from database import get_motivation, get_random_motivation

# Храним последние ответы пользователей
user_last_responses = {}

async def generate_motivation(message: Message):
    user_id = message.from_user.id
    user_input = message.text.lower()

    last_response = user_last_responses.get(user_id)  # Получаем последний ответ пользователя
    response = get_motivation(user_input, last_response)  # Передаём последний ответ

    if response:
        user_last_responses[user_id] = response  # Запоминаем новый ответ
        await message.answer(response)
    else:
        random_response = get_random_motivation()
        user_last_responses[user_id] = random_response  # Запоминаем случайную мотивацию
        await message.answer(random_response)

# Запуск бота
async def main():
    # Регистрируем обработчики
    dp.message.register(send_welcome, Command("start"))  # Фильтр для команды /start
    dp.message.register(generate_motivation)  # Фильтр для обычных сообщений

    # Удаляем старые сообщения перед запуском
    await bot.delete_webhook(drop_pending_updates=True)

    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
