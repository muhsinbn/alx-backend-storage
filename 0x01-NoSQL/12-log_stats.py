#!/usr/bin/env python3
""" A Script that provides stats about Nginx logs stored in MongoDB."""
from pymongo import MongoClient


def nginx_stats():
    """ The function to execute the script."""
    client = MongoClient('mongodb://127.0.0.1:27017')

    # Connect to the database and collection
    db = client['logs']
    collection = db['nginx']

    # get the number of documents in the collection
    total_logs = collection.estimated_document_count()

    # Print the total number of logs
    print(f"{total_logs} logs")

    # Print the method stats
    print("Methods:")

    # Get the unique methods using distinct()
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    # Use aggregate() to get the count for each method
    method_counts = list(collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]))

    for method in methods:
        count = next(
                (m for m in method_counts if m["_id"] == method),
                {"count": 0})["count"]
        print(f"\tmethod {method}: {count}")

    # Print the number of documents with method GET and path / status
    stats_check = collection.count_documents(
            {"method": "GET", "path": "/status"})
    print(f"{stats_check} status check")


if __name__ == "__main__":
    nginx_stats()
