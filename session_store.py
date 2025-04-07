import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_session(phone):
    data = r.get(phone)
    return json.loads(data) if data else []

def update_session(phone, user_msg, bot_msg):
    history = get_session(phone)
    history.append({"user": user_msg, "bot": bot_msg})
    r.set(phone, json.dumps(history, ensure_ascii=False))