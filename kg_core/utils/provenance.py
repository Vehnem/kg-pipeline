from pymongo import MongoClient
import datetime

class MongoProvenance():
    def __init__(self, db_name='local', collection_name='provenance', mongo_uri='mongodb://localhost:27017/'):
        client = MongoClient("mongodb://localhost:10000/")
        database = client["local"]
        # Check if the 'cache' collection exists; if not, create it
        if "cache" not in database.list_collection_names():
            database.create_collection("provenance")
        self.collection = database["provenance"]

    def get(self, key):
        result = self.collection.find_one({'_id': key})
        print(result)
        return result['result'] if result else None

    def set(self, prompt: str, completion: str, meta={}):
        meta.update({'timestamp': datetime.datetime.now()})
        self.collection.insert_one({'prompt': prompt, 'completion': completion, 'meta': meta})

class LLMCompletionProvenance():
    def __init__(self):
        pass