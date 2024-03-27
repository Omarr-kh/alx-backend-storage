#!/usr/bin/env python3
""" function that changes all topics of a school document """


def update_topics(mongo_collection, name, topics):
    """ update all with name=name """
    mongo_collection.update_many({"name": name},
                                 {"$set": {"topics": topics}})
