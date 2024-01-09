import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:10000/")
database = client["mydatabase"]
collection = database["persons"]

# Create collection if it doesn't exist
if "persons" not in database.list_collection_names():
    collection = database.create_collection("persons")

# Insert a simple item for a Person
person = {"name": "John Doe", "birthdate": "1990-01-01"}
collection.insert_one(person)
