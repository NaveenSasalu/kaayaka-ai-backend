import redis
import json
import os
from dotenv import load_dotenv

# Load .env first
load_dotenv()

# Connect to Redis
redis_client = redis.Redis.from_url(
    os.getenv("REDIS_URL"),
    decode_responses=True
)

def get_history(user_id: str):
    key = f"chat_history:{user_id}"
    data = redis_client.get(key)
    if data:
        return json.loads(data)
    return []

def save_message(user_id: str, message_obj: dict):
    key = f"chat_history:{user_id}"
    history = get_history(user_id)
    history.append(message_obj)
    redis_client.set(key, json.dumps(history))
