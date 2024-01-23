#!/usr/bin/env python3
"""a Python function that lists all documents in a collection:

Prototype: def list_all(mongo_collection):
Return an empty list if no document in the collection
mongo_collection will be the pymongo collection object
"""


def list_all(mongo_collection):
    """
    List all documents in a MongoDB collection.

    :param mongo_collection: pymongo collection object
    :return: List of documents in the collection
    """
    # Find all documents in the collection
    documents = mongo_collection.find()

    # Convert the documents to a list
    documents_list = list(documents)

    return documents_list


if __name__ == "__main__":
    # This part is for testing the function
    from pymongo import MongoClient

    # Connect to MongoDB server
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Specify the database and collection
    db = client.my_db
    school_collection = db.school

    # Get the list of all documents in the collection
    schools = list_all(school_collection)

    # Print the details of each document
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
