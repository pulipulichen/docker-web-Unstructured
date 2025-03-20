from .get_file_hash_key import get_file_hash_key
from .get_redis_client import get_redis_client
import json

import os
EXPIRE_DAY = float(os.getenv('CACHE_EXPIRE_DAY', 1.0))
EXPIRE_SECONDS = int(EXPIRE_DAY * 24 * 60 * 60)


def cache_set(chunk_config, file_path, data_dict):
  key = get_file_hash_key(chunk_config, file_path)
  redis_client = get_redis_client()

  redis_client.set(key, json.dumps(data_dict, ensure_ascii=False), ex=EXPIRE_SECONDS)
  return True