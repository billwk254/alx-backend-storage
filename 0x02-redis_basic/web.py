#!/usr/bin/env python3
"""
Module for retrieving HTML content from a URL and caching it with Redis.
"""


import requests
import redis
import time
from typing import str


def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a given URL and cache the result

    Args:
        url: The URL to retrieve the HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    # Initialize Redis connection
    redis_conn = redis.Redis()

    # Track the number of times the URL was accessed
    count_key = f"count:{url}"
    redis_conn.incr(count_key)

    # Check if the HTML content is already cached
    cached_content_key = f"content:{url}"
    cached_content = redis_conn.get(cached_content_key)

    if cached_content:
        return cached_content.decode('utf-8')

    # Retrieve the HTML content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the HTML content with an expiration time of 10 seconds
    redis_conn.setex(cached_content_key, 10, html_content)

    return html_content
