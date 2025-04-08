import redis
import json
import os

REDIS_URL = os.getenv("REDIS_URL")  # универсальный формат для Railway
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Выбираем подключение
if REDIS_URL:
    r = redis.from_url(REDIS_URL)
else:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def get_session(phone):
    data = r.get(phone)
    if data:
        return json.loads(data)
    return []

def update_session(phone, user_msg, bot_msg):
    history = get_session(phone)
    history.append({"user": user_msg, "bot": bot_msg})
    r.set(phone, json.dumps(history))