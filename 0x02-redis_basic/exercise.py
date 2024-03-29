#!/usr/bin/env python3
"""
Module for Cache class.
"""


import redis
import uuid
from typing import Union, Callable
from functools import wraps


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

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key and optionally apply a conversion function.

        Args:
            key: The key used to retrieve data from the cache.
            fn: Optional conversion function to apply to the retrieved data.

        Returns:
            Union[str, bytes, int, float, None]: The retrieved data, optionally converted based on the provided function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, bytes, None]:
        """
        Retrieve data from Redis as a string.

        Args:
            key: The key used to retrieve data from the cache.

        Returns:
            Union[str, bytes, None]: The retrieved data as a string.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, bytes, None]:
        """
        Retrieve data from Redis as an integer.

        Args:
            key: The key used to retrieve data from the cache.

        Returns:
            Union[int, bytes, None]: The retrieved data as an integer.
        """
        return self.get(key, fn=int)


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of times a method is called.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

# Decorate Cache.store with count_calls
Cache.store = count_calls(Cache.store)


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs for a particular function.

    Args:
        method: The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)

        # Store input arguments
        self._redis.rpush(input_key, str(args))

        # Execute the original method to get the output
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, output)

        return output

    return wrapper

# Decorate Cache.store with call_history
Cache.store = call_history(Cache.store)


def replay(method: Callable) -> None:
    """
    Display the history of calls for a particular function.

    Args:
        method: The method whose history of calls is to be displayed.
    """
    input_key = "{}:inputs".format(method.__qualname__)
    output_key = "{}:outputs".format(method.__qualname__)

    inputs = [eval(args.decode('utf-8')) for args in cache._redis.lrange(input_key, 0, -1)]
    outputs = [output.decode('utf-8') for output in cache._redis.lrange(output_key, 0, -1)]

    print(f"{method.__qualname__} was called {len(inputs)} times:")
    for input_args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_args}) -> {output}")

if __name__ == "__main__":
    # Example usage
    cache = Cache()
    cache.store("foo")
    cache.store("bar")
    cache.store(42)
    replay(cache.store)
