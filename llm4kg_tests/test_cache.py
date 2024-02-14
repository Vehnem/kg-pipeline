###Test cache implementations.###
import time
from llm4kg_core.utils.cache import MongoCache, CacheDecorator

mongo_cache = MongoCache()
cache_decorator = CacheDecorator(mongo_cache)

@cache_decorator.cached
def __calculate(x, y):
    time.sleep(0.1*x*y)
    return x * y

def test_mongo_cache():
    print()

    result1 = __calculate(2, 3)
    print(str(time.time())+" Result 1:", result1)

    result2 = __calculate(3, 2)  # This should retrieve the result from cache
    print(str(time.time())+" Result 2:", result2)

    result3 = __calculate(2, 3)  # This will calculate and store a new result
    print(str(time.time())+" Result 3:", result3)
