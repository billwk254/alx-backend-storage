#!/usr/bin/env python3
"""
Update topics of a school document based on the name:

Prototype: def update_topics(mongo_collection, name, topics):
mongo_collection will be the pymongo collection object
name (string) will be the school name to update
topics (list of strings) will be the list of topics approached in the school
"""


def update_topics(mongo_collection, name, topics):
    """
    Update topics of a school document based on the name.

    :param mongo_collection: pymongo collection object
    :param name: School name to update
    :param topics: List of topics to set for the school
    """
    # Update the topics of the school with the specified name
    mongo_collection.update_one({'name': name}, {'$set': {'topics': topics}})
