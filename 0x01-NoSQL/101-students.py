#!/usr/bin/env python3
""" Python Function that returns all students sorted by average score."""
from pymongo import MongoClient


def top_students(mongo_collection):
    """ Returns sorted and average score must be part of each item
    returns with key = averageScore
    """
    if mongo_collection is None:
        return []
    pipeline = [
            {
                "$project": {
                    "name": 1,
                    "topics": 1,
                    "averageScore": {"$avg": "$topics.score"}
                }
            },
            {
                "$sort": {"averageScore": -1}
            }
    ]
    return list(mongo_collection.aggregate(pipeline))
