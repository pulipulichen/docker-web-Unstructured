import redis
import os

redis_client = None

def get_redis_client():
  global redis_client
  if redis_client is None:
    # 連接 Redis
    redis_client = redis.Redis(
      host=os.getenv('REDIS_HOST', 'redis'), 
      port=int(os.getenv('REDIS_PORT',6379)), 
      decode_responses=True
    )

  return redis_client
