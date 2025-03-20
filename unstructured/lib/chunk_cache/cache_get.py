from .get_file_hash_key import get_file_hash_key
from .get_redis_client import get_redis_client
import json
import os

def cache_get(chunk_config, file_path):
  if os.getenv('CACHE_ENABLED', "True").lower() != "true":
    return None
  # return None

  key = get_file_hash_key(chunk_config, file_path)
  redis_client = get_redis_client()

  if redis_client.exists(key):
    return json.loads(redis_client.get(key))
  else:
    return None