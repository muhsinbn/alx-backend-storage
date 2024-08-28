#!/usr/bin/env python3
""" Function that returns the list of school having specific topic."""
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """ Returns list of school and topic will be searched."""
    if mongo_collection is None:
        return []
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
