#!/usr/bin/env python3
"""
Return the list of schools having a specific topic:

Prototype: def schools_by_topic(mongo_collection, topic):
mongo_collection will be the pymongo collection object
topic (string) will be topic searched
"""


def schools_by_topic(mongo_collection, topic):
    """
    Return the list of schools having a specific topic.

    :param mongo_collection: pymongo collection object
    :param topic: Topic to search for
    :return: List of schools matching the specified topic
    """
    # Find schools that have the specified topic
    schools = mongo_collection.find({'topics': topic})

    # Convert the result to a list
    schools_list = list(schools)

    return schools_list
