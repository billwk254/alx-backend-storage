#!/usr/bin/env python3
"""
Return all students sorted by average score:

Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
"""


from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Return all students sorted by average score.

    :param mongo_collection: pymongo collection object
    :return: List of students sorted by average score
    """
    # Aggregate pipeline to calculate the average score
    pipeline = [
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "topics": 1,
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    # Execute the aggregation pipeline
    result = list(mongo_collection.aggregate(pipeline))

    return result
