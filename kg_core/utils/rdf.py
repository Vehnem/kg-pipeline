from kg_core.utils.annotation import todo
import json

# TODO duplciate entries ... order
def common_prefix_map():    
    with open('resources/context.jsonld', 'r') as f:
        context = json.load(f)
        return context["@context"]


# @todo("move to tests")
# def test():
#     context = common_prefix_map()
#     print(context)

# test()

