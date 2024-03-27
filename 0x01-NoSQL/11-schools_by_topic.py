#!/usr/bin/env python3
""" function returns list of school having a specific topic """


def schools_by_topic(mongo_collection, topic):
    """ list of school having a specific topic """
    schools = mongo_collection.find({"topics": {"$in": [topic]}})
    return schools
