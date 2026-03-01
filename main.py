import json

from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ChatAction
from aiogram.types import Message

import asyncio
import dotenv
import os

import AdminPanel
from AdminPanel import admin_request, is_admin, init_admin_panel
from OpenAIManager import OpenAIManager
from tools import Database
from utility import MessageWaiter

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
router = Router()
dp.include_router(router)
dp.include_router(AdminPanel.router)

bot = Bot(BOT_TOKEN)

mw = MessageWaiter()

@router.message()
async def message_handler(message: Message):
    if message.text[0] == "/":
        await command_handler(message)
    else:
        await user_request(message)

async def command_handler(message: Message):
    if message.text == "/start":
        if is_admin(message):
            await init_admin_panel(bot, message)
        else:
            await start(message)

        await AI.create_user(message)

    else:
        await bot.send_message(message.chat.id, "Такой команды не существует")

async def start(message: Message):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Привет! Как у тебя настроение?"
    )

async def user_request(message: Message):
    if is_admin(message):
        if not await admin_request(bot, database, message):
            return

    await mw.on_message(message.chat.id, message.text)

    prompt = await mw.get_message(message.chat.id)

    prompt_message = Message(
        chat=message.chat,
        text=prompt,
        message_id=message.message_id,
        date=message.date
    )

    if mw.lock.locked():
        return

    await bot.send_chat_action(chat_id=message.chat.id, action=ChatAction.TYPING)
    ai_ans = await AI.ask(prompt_message)

    if ai_ans[-1] == "оператор":
        clients = database.get("clients")
        if not clients:
            clients = set()
        else:
            clients = set(clients)
        clients.add(str(message.chat.id))
        database.set("clients", list(clients))
        ai_ans = ai_ans[:-1]
        for admin_id in json.loads(os.getenv("ADMIN_IDS")):
            await bot.send_message(
                admin_id,
                f"Пользователь [{message.chat.first_name}](tg://user?id={message.chat.id}) хочет заказать массаж",
                parse_mode="MarkdownV2"
            )

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