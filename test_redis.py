import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

try:
    print(r.ping())
except Exception as e:
    print("Error:", e)
