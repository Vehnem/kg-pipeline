import hashlib
import json

def Sha512Hash(Password):
    HashedPassword=hashlib.sha512(Password.encode('utf-8')).hexdigest()
    return str(HashedPassword)


def hashDict(dict):
    # sort the dictionary and hash
    return Sha512Hash(json.dumps(dict, sort_keys=True))