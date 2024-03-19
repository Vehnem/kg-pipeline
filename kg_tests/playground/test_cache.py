###Test cache implementations.###
import time, random
from kg_core.utils.cache import MongoCache, CacheDecorator

mongo_cache = MongoCache()
cache_decorator = CacheDecorator(mongo_cache)

@cache_decorator.cached
def __excute_prompt(prompt, model_name, **kwargs):
    time.sleep(0.1)
    return random.randint(0, 100)

def test_mongo_cache():
    print()

    result1 = __excute_prompt('Prompt1', 'GPT4' , kwarg1="some_value", kwarg2={'nested_key1':'nested_value1', 'nested_key2':'nested_value2'})
    print(str(time.time())+" Result 1:", result1)

    # result2 = __excute_prompt('Promtp2', 'GPT4') 
    # print(str(time.time())+" Result 2:", result2)

    result3 = __excute_prompt('Prompt1', 'GPT4', kwarg2={'nested_key2':'nested_value2', 'nested_key1':'nested_value1'}, kwarg1="some_value") 
    print(str(time.time())+" Result 3:", result3)
