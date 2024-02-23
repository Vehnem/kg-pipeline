from functools import wraps
from abc import ABC, abstractmethod
from pymongo import MongoClient
from .hash import Sha512Hash

class Cache(ABC):
    @abstractmethod
    def get(self, key):
        pass
    
    @abstractmethod
    def set(self, key, value):
        pass

class MongoCache(Cache):
    def __init__(self, db_name='local', collection_name='cache', mongo_uri='mongodb://localhost:27017/'):
        client = MongoClient("mongodb://localhost:10000/")
        database = client["local"]
        # Check if the 'cache' collection exists; if not, create it
        if "cache" not in database.list_collection_names():
            database.create_collection("cache")
        self.collection = database["cache"]

    def get(self, key):
        result = self.collection.find_one({'_id': key})
        return result['result'] if result else None

    def set(self, key, value):
        self.collection.insert_one({'_id': key, 'result': value})

class RedisCache(Cache):
    def __init__(self, host='localhost', port=6379, db=0):
        import redis
        self.client = redis.StrictRedis(host=host, port=port, db=db)

    def get(self, key):
        result = self.client.get(key)
        return result.decode() if result else None

    def set(self, key, value):
        self.client.set(key, value)

class CacheDecorator:
    def __init__(self, cache):
        self.cache = cache

    def cached(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = Sha512Hash(str((args, frozenset(kwargs.items()))))
            record = self.cache.get({'_id': key})
            if record is None:
                print("result is none")
                result = func(*args, **kwargs)
                self.cache.set({'_id': key, 'result': result})
                return result
            else:
               return record['result']
        
        return wrapper