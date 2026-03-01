import json
import os

import redis

class Database:
    def __init__(self):
        self.r = redis.Redis(
            host="localhost",
            port=6379,
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True
        )
        if not self.r.exists("conversations"):
            self.r.set("conversations", json.dumps({}))

    def get(self, key):
        return json.loads(self.r.get(key))

    def set(self, key, value):
        return self.r.set(key, json.dumps(value))

# r.set("test", "hello")
# print(r.get("test"))