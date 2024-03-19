from pymongo import MongoClient

def test_mongodb():
    mongo = MongoClient("mongodb://localhost:10000/")
    coll = mongo['local'].get_collection('cache')

    res = list(coll.find())

    for re in res:
        print()
        print('#####')
        print()
        print(re['result']['return_value'])
