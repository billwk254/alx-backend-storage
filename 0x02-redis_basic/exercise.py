#!/usr/bin/env python3
"""
Module for Cache class.
"""


import redis
import uuid
from typing import Union


class Cache:
    """
    Cache class for storing data in Redis.
    """

    def __init__(self):
        """
        Initialize the Cache object with a Redis client instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store input data in Redis with a randomly generated key.

        Args:
            data: Data to be stored in the cache.

        Returns:
            str: The randomly generated key used to store the data in Redis.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
