### Test Higherorder Functions in Python ###
import time, calendar
from kg_core.utils.cache import cached

def dummy_function(x: str):
    return x


def apply_fun(fun, x: str):
    return fun(x)


def test_function_as_parameter():
    print(apply_fun(dummy_function, "hello"))


@cached
def __costly_function(t):
    time.sleep(t)
    return str(t)+"s"
    

def test_cached_annotation():
    print()
    print(time.time())
    __costly_function(0.1)
    print(time.time())
    __costly_function(0.1)
    print(time.time())
    __costly_function(0.2)
    print(time.time())
    pass