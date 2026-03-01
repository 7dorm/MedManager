from aiogram import Bot, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardButton
import json
import os

router = Router()


@router.message()
async def admin_request(bot: Bot, database, message: Message):
    if message.text == 'Проверить клиентов':
        clients = database.get("clients")
        if clients:
            keyboard = []

            for i in range(0, len(clients)):
                keyboard.append(
                    InlineKeyboardButton(
                        text=clients[i],
                        callback_data=f"clients_{clients[i]}"
                    )
                )


            markup = InlineKeyboardMarkup(
                inline_keyboard=[keyboard]
            )

            await bot.send_message(
                message.chat.id,
                "Вот список всех клиентов которые хотели услугу:",
                reply_markup=markup
            )
        else:
            await bot.send_message(
                message.chat.id,
                "Пока нет клиентов"
            )
    else:
        return True

@router.callback_query()
async def callback_query(callback: CallbackQuery):
    if callback.data.startswith("clients_"):
        await callback.message.edit_text(
            text=f"Нажмите на [профиль клиента](tg://user?id={callback.data.replace('clients_', '')}) чтобы написать ему",
            parse_mode="MarkdownV2"
        )
    await callback.answer()

async def init_admin_panel(bot: Bot, message: Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Проверить клиентов")
            ]
        ],
        resize_keyboard=True
    )

    await bot.send_message(
        message.chat.id,
        "Hello admin",
        reply_markup=markup
    )

def is_admin(message: Message):
    return message.chat.id in json.loads(os.getenv("ADMIN_IDS", "[]"))