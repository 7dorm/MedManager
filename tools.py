import redis
from redis.exceptions import ResponseError
import json
import os

class Database:
    def __init__(self):
        self.r = redis.Redis(
            host="localhost",
            port=6379,
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )

    def reset(self):
        self.r.flushdb()

    def get(self, name):
        item = self.r.get(name)
        if item:
            return json.loads(item)
        return item

    def set(self, name, value):
        self.r.set(name, json.dumps(value))