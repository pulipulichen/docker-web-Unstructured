from .get_file_hash_key import get_file_hash_key
from .get_redis_client import get_redis_client
import json
import os

def cache_get(item_id, file_path):
  if os.getenv('CACHE_ENABLED', "True").lower() != "true":
    return None
  # return None

  key = get_file_hash_key(item_id, file_path)
  redis_client = get_redis_client()

  if redis_client.exists(key):
    return json.loads(redis_client.get(key))
  else:
    return None