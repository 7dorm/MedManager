from openai import AsyncOpenAI

from Manager import Manager

class OpenAIManager(Manager):
    def __init__(self, token, model, n_max=10):
        super().__init__(token, model, n_max)
        self.client = AsyncOpenAI(api_key=token)
