from collections import defaultdict
import asyncio

class MessageWaiter:
    def __init__(self, timeout=5):
        self.timers = defaultdict()
        self.buffers = defaultdict()
        self.output = defaultdict()
        self.timeout = timeout
        self.lock = asyncio.Lock()

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
            self.lock.release()

        if chat_id in self.timers and self.timers[chat_id]:
            self.timers[chat_id].cancel()

        self.timers[chat_id] = asyncio.create_task(timer())

        await self.lock.acquire()

    async def get_message(self, user_id):
        async with self.lock:
            return self.output[user_id]


def format_response(response):
    print(response)
    return list(map(lambda x: x.strip(), response.replace("\n\n", "^").split("^")))

