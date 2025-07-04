import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Use decode_responses=True to avoid byte-string issues
