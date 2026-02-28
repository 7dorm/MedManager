import os

from aiogram.types import Message
from utility import format_response

class Manager:
    def __init__(self, token, model, n_max = 10):
        self.conversation = {}
        self.n_max = n_max
        self.client = None
        self.model = model

    def create_user(self, message: Message):
        self.conversation[message.chat.id] = [{
            "role": "system",
            "content": os.getenv("SYSTEM_PROMPT")
        }, {
            "role": "assistant",
            "content": "Привет! Как у тебя настроение?"
        }]

    async def ask(self, message: Message):
        if self.client:
            self.conversation[message.chat.id].append({"role": "user", "content": message.text})
            if len(self.conversation[message.chat.id]) >= self.n_max * 2 + 1:
                self.conversation[message.chat.id].pop(1)
                self.conversation[message.chat.id].pop(1)
            res = await self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation[message.chat.id]
            )

            response = res.choices[0].message.content

            self.conversation[message.chat.id].append({"role": "assistant", "content": response})

            return format_response(response)
        return "None"