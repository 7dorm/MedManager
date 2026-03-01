from aiogram import Bot, Dispatcher
from aiogram.enums import ChatAction
from aiogram.types import Message

import asyncio
import dotenv
import os

from OpenAIManager import OpenAIManager
from OpenRouterManager import OpenRouterManager
from tools import Database

# ENV
dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_API")
OPENROUTER_API = os.getenv("OPENROUTER_API")

# Database
database = Database()

# OpenAI
AI = OpenAIManager(
    OPENAI_TOKEN,
   "gpt-4o-mini",
    database
)

# Aiogram
dp = Dispatcher()
bot = Bot(BOT_TOKEN)

@dp.message()
async def start(message: Message):
    if message.text == "/start":
        await bot.send_message(chat_id=message.chat.id, text="Привет! Как у тебя настроение?")
        AI.create_user(message)
    else:
        await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

        ai_ans = await AI.ask(message)

        if ai_ans[-1] == "оператор":
            print(message.chat.id)
            ai_ans = ai_ans[:-1]

        for ans in ai_ans[:-1]:
            await asyncio.sleep(len(ans)/20)
            await bot.send_message(chat_id=message.chat.id, text=ans)
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

        await asyncio.sleep(len(ai_ans[-1])/20)
        await bot.send_message(chat_id=message.chat.id, text=ai_ans[-1])

async def main():
    print("Started polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())