import json
import logging
import os
from news.models import Post
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


def redis_set_new_posts(post: Post):
    redis_conn.hset(
        name='new_posts',
        key=post.pk,
        value=post.category.title
    )


def redis_set_popular_posts_of_day(post: Post):
    redis_conn.hset(
        name='posts_of_day',
        key=post.pk,
        value=post.title
    )


def redis_set_popular_posts_of_week(post: Post):
    redis_conn.hset(
        name='posts_of_week',
        key=post.pk,
        value=post.title
    )


def _redis_get_new_posts():
    new_posts = {}
    data = redis_conn.hgetall('new_posts')
    for key, value in data.items():
        new_posts.setdefault(value.decode('utf-8'), []).append(int(key))
    redis_conn.delete('new_posts')
    if new_posts:
        return new_posts
    return {}


def redis_get_popular_posts_of_day():
    posts_of_a_day = {}
    data = redis_conn.hgetall('posts_of_day')
    for key, value in data.items():
        posts_of_a_day.setdefault(key.decode('utf-8'), value.decode('utf-8'))
    redis_conn.delete('posts_of_day')
    if posts_of_a_day:
        return posts_of_a_day
    return {}


def redis_get_popular_posts_of_week():
    posts_of_a_week = {}
    data = redis_conn.hgetall('posts_of_week')
    for key, value in data.items():
        posts_of_a_week.setdefault(key.decode('utf-8'), value.decode('utf-8'))
    redis_conn.delete('posts_of_week')
    if posts_of_a_week:
        return posts_of_a_week
    return {}


def _clear_key(names):
    """Delete one or more keys specified by ``names``"""
    redis_conn.delete(names)
