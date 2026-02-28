from openai import AsyncOpenAI
from aiogram.types import Message
import dotenv
import os

dotenv.load_dotenv()


def format_response(response):
    return list(map(lambda x: x.strip(), response.split("^")))


class Manager:
    def __init__(self, token, n_max = 10):
        self.client = AsyncOpenAI(api_key=token)
        self.conversation = {}
        self.n_max = n_max

    def create_user(self, message: Message):
        self.conversation[message.chat.id] = []

    async def ask(self, message: Message):
        self.conversation[message.chat.id].append({"role": "user", "content": message.text})
        if len(self.conversation[message.chat.id]) >= self.n_max * 2 + 1:
            self.conversation[message.chat.id].pop(1)
            self.conversation[message.chat.id].pop(1)
        res = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.conversation[message.chat.id]
        )

        response = res['choices'][0]['message']['content']

        self.conversation[message.chat.id].append({"role": "assistant", "content": response})

        return format_response(response)

