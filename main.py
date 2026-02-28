from aiogram import Bot, Dispatcher
from aiogram.enums import ChatAction
from aiogram.types import Message
from Manager import Manager

import asyncio
import os

# ENV
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")

# OpenAI
AI = Manager(OPENAI_TOKEN)

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

        ai_ans = await AI.ask(message.text)

        if ai_ans[-1] == "оператор":
            print(message.chat.id)
            ai_ans = ai_ans[:-1]

        for ans in ai_ans:
            await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)

            await asyncio.sleep(len(ans)/6)

            await bot.send_message(chat_id=message.chat.id, text=ans)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())