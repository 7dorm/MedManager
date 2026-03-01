from openai import AsyncOpenAI

from Manager import Manager

class OpenAIManager(Manager):
    def __init__(self, token, model, database, n_max=10):
        super().__init__(token, model, database, n_max)
        self.client = AsyncOpenAI(api_key=token)
