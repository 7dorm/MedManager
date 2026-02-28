from collections import defaultdict

import asyncio


def format_response(response):
    print(response)
    return list(map(lambda x: x.strip(), response.split("^")))


class MessageWaiter:
    def __init__(self, timeout=5):
        self.timers = defaultdict()
        self.buffers = defaultdict()
        self.output = defaultdict()
        self.timeout = timeout

    async def process_message(self, user_id):
        self.output[user_id] = self.buffers[user_id]
        self.buffers[user_id] = ""

    async def on_message(self, chat_id, message):
        if chat_id in self.buffers:
            self.buffers[chat_id] += message + " "
        else:
            self.buffers[chat_id] = message + " "

        async def timer():
            await asyncio.sleep(self.timeout)
            await self.process_message(chat_id)

        if chat_id in self.timers and self.timers[chat_id]:
            self.timers[chat_id].cancel()

        self.timers[chat_id] = asyncio.create_task(timer())

async def test():
    temp = MessageWaiter()
    await temp.on_message(1, "hello")
    await asyncio.sleep(1)
    await temp.on_message(1, "world")


if __name__ == "__main__":
    asyncio.run(test())
