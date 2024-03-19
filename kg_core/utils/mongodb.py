from pymongo import MongoClient
from bson.objectid import ObjectId
from kg_core.utils.log import Logger

log = Logger("MongoDB")

class MongoConnection:

    def __init__(self, db_name='local', mongo_uri='mongodb://localhost:27017/'):
        client = MongoClient(mongo_uri)
        self.database = client[db_name]
        self.collections = list(self.database.list_collection_names())

        # Check if the 'cache' collection exists; if not, create it
        # if "cache" not in self.database.list_collection_names():
        #     self.database.create_collection(collection_name)
        # self.collection = self.database[collection_name]    

    def coll(self, collection_name):
        if collection_name not in self.collections:
            self.database.create_collection(collection_name)
            self.collections.append(collection_name)
        return self.database[collection_name]

    def list_collections(self):
        return self.collections

    def get(self, collection_name, query_doc: dict):
        result = self.coll(collection_name).find_one(query_doc)
        return result if result else None
    
    def getAll(self, collection_name):
        result = self.coll(collection_name).find()
        return result

    def set(self, collection_name, doc):
        self.coll(collection_name).insert_one(doc)

    def update(self, collection_name, doc, upsert=False):
        # log.debug(doc)
        self.coll(collection_name).update_one({'_id': doc['_id']}, {'$set': doc}, upsert=upsert)

    def insert(self, collection_name, doc):
        log.debug(f"inserting into {collection_name}")
        self.coll(collection_name).insert_one(doc)

    def removeById(self, collection_name, id):
        self.coll(collection_name).delete_one({'_id': ObjectId(id)})

    def drop(self, collection_name):
        if collection_name in self.collections:
            self.coll(collection_name).drop()