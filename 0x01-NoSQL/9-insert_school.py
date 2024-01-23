#!/usr/bin/env python3
"""
Write a Python function that inserts a new document
in a collection based on kwargs:

Prototype: def insert_school(mongo_collection, **kwargs):
mongo_collection will be the pymongo collection object
Returns the new _id
"""


from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document in a MongoDB collection based on kwargs.

    :param mongo_collection: pymongo collection object
    :param kwargs: Key-value pairs for the document fields
    :return: The new _id of the inserted document
    """
    # Insert the document into the collection and get the _id
    new_school_id = mongo_collection.insert_one(kwargs).inserted_id

    return new_school_id


if __name__ == "__main__":
    # This part is for testing the function
    from 8-all import list_all

    # Connect to MongoDB server
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Specify the database and collection
    db = client.my_db
    school_collection = db.school

    # Insert a new school document
    new_school_id = insert_school(school_collection, name="UCSF", address="505 Parnassus Ave")
    print("New school created: {}".format(new_school_id))

    # List all schools to verify the insertion
    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'), school.get('name'), school.get('address', "")))
