import json
import logging
import os

from django.conf import settings

import redis as redis

logger = logging.getLogger('process')

redis_conn = redis.Redis(host=os.getenv('REDIS_HOST', '127.0.0.1'),
                         port=int(os.getenv('REDIS_PORT', 6379)),
                         db=int(os.getenv('REDIS_DBT', 0)))


def _redis_get_summary_profile_data(cache_key: str):
    """Get summary profile data"""
    return redis_conn.get(cache_key)


def _redis_set_summary_profile_data(cache_key: str, data: dict):
    """Set summary profile data"""
    redis_conn.set(name=cache_key, value=json.dumps(data, indent=4, sort_keys=True, default=str),
                   ex=settings.SUMMARY_PROFILE_DATA_REDIS_EXPIRE_TIME)


def _clear_key(names):
    """Delete one or more keys specified by ``names``"""
    redis_conn.delete(names)
