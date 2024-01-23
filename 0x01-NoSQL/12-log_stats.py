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

from pymongo import MongoClient

def log_stats(mongo_collection):
    """
    Display stats about Nginx logs stored in MongoDB.

    :param mongo_collection: pymongo collection object
    """
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {mongo_collection.count_documents({'method': method})}")

    print(f"{mongo_collection.count_documents({'method': 'GET', 'path': '/status'})} status check")
