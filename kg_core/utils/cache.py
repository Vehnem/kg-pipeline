from functools import wraps
from abc import ABC, abstractmethod
from pymongo import MongoClient
from .hash import Sha512Hash, hashDict
import json
import datetime

class Cache(ABC):
    @abstractmethod
    def get(self, key):
        pass
    
    @abstractmethod
    def set(self, key, value):
        pass

    def insert(self, value):
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
        # print(result)
        return result['result'] if result else None

    def set(self, key, value):
        self.collection.insert_one({'_id': key, 'result': value})

    def insert(self, value):
        self.collection.insert_one({'result': value})


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
            key = Sha512Hash(str((args, json.dumps(kwargs, sort_keys=True))))
            record = self.cache.get(key)
            if record is None:
                return_value = func(*args, **kwargs)
                self.cache.set(key,{'args': args, 'kwargs': kwargs, 'return_value': return_value, 'timestamp': datetime.datetime.now()})
                return return_value
            else:
               return record['return_value']
        
        return wrapper

    def persist(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return_value = func(*args, **kwargs)
            self.cache.insert({'args': args, 'kwargs': kwargs, 'return_value': return_value, 'timestamp': datetime.datetime.now()})
            return return_value
        return wrapper