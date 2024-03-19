from kg_core.utils.mongodb import MongoConnection
import json

mongo = MongoConnection(mongo_uri='mongodb://localhost:10000/')


# id, prev, next
# 1, None, None
# 2, None, 3
# 3, 2, None
# 4, None, 5
# 5, 4, 6
# 6 , 5, None

# start ids are 1, 2, 4

def test_extract_overall():
    results = list(mongo.getAll('journal_final'))
    resultsByModel = {}

    for result in results:
        model = result['meta']['model']
        if model not in resultsByModel:
            resultsByModel[model] = []
        resultsByModel[model].append(result)

    for model, results in resultsByModel.items():
        print(model)
        extract_overall(results)


def extract_overall(results):

    # results = list(mongo.getAll('journal_2024_03_11T14_36_07'))

    print(len(results))

    ids = set()
    start_ids = set()
    nextIdOf = {}
    prevIdOf = {}
    idIsValid = {}

    buckets = {
        "no_rep": []
        , "one_rep": []
        , "two_rep": []
        , "un_rep" : []
    }

    counts = {
        "no_rep": 0
        , "one_rep": 0
        , "two_rep": 0
        , "un_rep" : 0
        # , "with_prev_hash" : 0
        # , "no_rep_test" : 0
    }


    def sort_results_on_timestamp(results):
        return sorted(results, key=lambda x: x['meta']['timestamp'])
    
    prev_id = None
    for x in sort_results_on_timestamp(results):
        _id = str(x.get('_id', None))
        ids.add(_id)
        prev_hash = x.get('meta', None).get('prev_hash', None)
        idIsValid[_id] = x.get('meta', None).get('misc', None).get('valid_rdf', None)
        if prev_hash:
            nextIdOf[prev_id] = _id
            prevIdOf[_id] = prev_id
            # if x.get('meta', None).get('misc', None).get('valid_rdf', None):
            #     counts["with_prev_hash"] += 1
        else:
            start_ids.add(_id)
            # if x.get('meta', None).get('misc', None).get('valid_rdf', None):
            #     counts["no_rep_test"] += 1
        
        prev_id = _id

    for id in start_ids:
        if id in nextIdOf.keys():
            # > 1 repair
            hop1 = nextIdOf[id]
            if hop1 in nextIdOf:
                # > 2 repairs
                hop2 = nextIdOf[hop1]
                if idIsValid[hop2]:
                    buckets["two_rep"].append(hop2)
                    counts["two_rep"] += 1
                else :
                    buckets["un_rep"].append(hop2)
                    counts["un_rep"] += 1
            else:
                buckets["one_rep"].append(hop1)
                counts["one_rep"] += 1
        else:
            buckets["no_rep"].append(id)
            counts["no_rep"] += 1


    # print(json.dumps(nextIdOf, indent=2))
    # print("next id of", str(len(nextIdOf)))

    # print(json.dumps(prevIdOf, indent=2))
    # print("prev id of", str(len(prevIdOf)))

    print(json.dumps(counts, indent=2))
    print("total counts", sum(counts.values()))

    # print('ids', len(ids))
    # print('start ids', len(start_ids))
    # print(json.dumps(buckets, indent=2))
