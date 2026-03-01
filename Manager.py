from openai import AsyncOpenAI
import os

from aiogram.types import Message
from utility import format_response

class Manager:
    client: AsyncOpenAI
    def __init__(self, token, model, database, n_max = 10):
        self.n_max = n_max
        self.model = model
        self.database = database

    def create_user(self, message: Message):
        conv = self.database.get("conversations")
        conversation = [{
            "role": "system",
            "content": os.getenv("SYSTEM_PROMPT")
        }, {
            "role": "assistant",
            "content": "Привет! Как у тебя настроение?"
        }]

        conv[str(message.chat.id)] = conversation
        self.database.set("conversations", conv)

    async def ask(self, message: Message):
        if self.client:
            conversation = self.database.get("conversations")
            user_id = str(message.chat.id)
            conversation[user_id].append({"role": "user", "content": message.text})
            if len(conversation[user_id]) >= self.n_max * 2 + 1:
                conversation[user_id].pop(1)
                conversation[user_id].pop(1)
            res = await self.client.chat.completions.create(
                model=self.model,
                messages=conversation[user_id]
            )

            response = res.choices[0].message.content

            conversation[user_id].append({"role": "assistant", "content": response})
            self.database.set("conversations", conversation)

            return format_response(response)
        return "None"