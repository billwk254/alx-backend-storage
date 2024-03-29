#!/usr/bin/env python3
"""
Improved version of 12-log_stats.py with top 10 most present IPs:

Database: logs
Collection: nginx

Display:
    first line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents
    one line with the number of documents
        method=GET
        path=/status
    third line: IPs:
    10 lines with the IP
"""


from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Display improved stats about Nginx logs stored in MongoDB.

    :param mongo_collection: pymongo collection object
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx
    total = logs_collection.count_documents({})
    get = logs_collection.count_documents({"method": "GET"})
    post = logs_collection.count_documents({"method": "POST"})
    put = logs_collection.count_documents({"method": "PUT"})
    patch = logs_collection.count_documents({"method": "PATCH"})
    delete = logs_collection.count_documents({"method": "DELETE"})
    path = logs_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")
    print("IPs:")
    sorted_ips = logs_collection.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    i = 0
    for s in sorted_ips:
        if i == 10:
            break
        print(f"\t{s.get('_id')}: {s.get('count')}")
        i += 1
