from aiogram import Bot, Dispatcher
from aiogram.types import Message

import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")


dp = Dispatcher()

bot = Bot(BOT_TOKEN)

@dp.message()
async def start(message: Message):
    await bot.send_message(chat_id=message.chat.id, text=message.text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())