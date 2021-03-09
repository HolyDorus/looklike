import redis

from looklike.configs import config


redis_client = redis.Redis.from_url(config.REDIS_URL)


def format_cache_key(clothes_ids: list[int]) -> str:
    cache_key = 'search_character_'
    for i, clothes_id in enumerate(clothes_ids):
        cache_key += str(clothes_id)
        if (i < len(clothes_ids) - 1):
            cache_key += ','
    return cache_key
