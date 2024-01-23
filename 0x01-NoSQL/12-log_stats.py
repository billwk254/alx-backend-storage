#!/usr/bin/env python3
"""
Stats about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx

Display:
    first line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents with the method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    one line with the number of documents with:
        method=GET
        path=/status
"""


import pymongo
from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Display stats about Nginx logs stored in MongoDB.

    :param mongo_collection: pymongo collection object
    """
    print(f"{mongo_collection.estimated_document_count()} logs")

    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    number_of_gets = mongo_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{number_of_gets} status check")


if __name__ == "__main__":
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx
    log_nginx_stats(mongo_collection)