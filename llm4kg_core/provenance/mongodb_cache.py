"""LLM cache implenetatin with MongoDB backend."""
import pymongo
from functools import wraps

# TODO the _id can be hash all input parameters
class MongoCache():

    def __init__(self, collection):
        client = pymongo.MongoClient("mongodb://localhost:10000/")
        database = client["local"]
        # Check if the 'cache' collection exists; if not, create it
        if "cache" not in database.list_collection_names():
            database.create_collection("cache")
        self.collection = database["cache"]


    def cached(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            key = str((args, frozenset(kwargs.items())))
            result = self.collection.find_one({'_id': key})
            if result is None:
                result = func(*args, **kwargs)
                self.collection.insert_one({'_id': key, 'result': result})
            return result['result']
        
        return wrapper


# # Connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:10000/")
# database = client["mydatabase"]
# collection = database["persons"]

# # Create collection if it doesn't exist
# if "persons" not in database.list_collection_names():
#     collection = database.create_collection("persons")

# # Insert a simple item for a Person
# person = {"name": "John Doe", "birthdate": "1990-01-01"}
# collection.insert_one(person)
