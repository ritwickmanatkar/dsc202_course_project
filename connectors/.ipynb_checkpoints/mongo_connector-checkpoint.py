from pymongo import MongoClient
from auth.connector_auth import mongo_host, mongo_port


def get_mongo_connection():
    """ This returns the mongo connection"""
    return MongoClient(
        host=mongo_host,
        port=mongo_port
    )
