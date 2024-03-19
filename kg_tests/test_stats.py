from kg_core.utils.mongodb import MongoConnection
from kg_core.utils.output_parser import CodeBlockExtractor
from kg_tasks.map.rml_mapper import RMLMapperJavaImpl
from kg_tasks.map.rml_util import RML_Wrapper
from kg_core.utils.cache import MongoCache, CacheDecorator
from kg_core.metrics.metrics import RML_Evaluation
from kg_tasks.repair.rdfrepair import TurtleRepair
from rdflib import Graph
from collections import defaultdict
import time
import json
import os
import csv
import pandas as pd
from bson import json_util

mongo = MongoConnection(mongo_uri='mongodb://localhost:10000/')

import warnings
warnings.filterwarnings("ignore", message=f".*does not look like a valid URI.*")

FINAL_COLLECTION="journal_final"
FINAL_EVALUATION="evaluation_final"

mongoCache = MongoCache()
cache = CacheDecorator(mongoCache)

JOURNAL = "journal_2024_03_11T14_36_07"
JOURNAL = "journal_2024_03_11T15_27_44"

# CONST
FIGURE_DIR = "figures"

def test_prepare_stats():
    journals = ["journal_final_claude21","journal_final_claude3","journal_final_gpt35","journal_final_gpt4turbo","journal_final_geminipro"]

    mongo.drop(FINAL_COLLECTION)

    cnt = 0
    for journal in journals:
        results = list(mongo.getAll(journal))
        for result in results:
            del result['_id']
            mongo.insert(FINAL_COLLECTION,result)
            cnt += 1
    print('cnt', cnt)

@cache.cached
def execute_mapping(idx, model_name, mapping_data, snippet_id) -> str:

    rml_graph = Graph().parse(data=mapping_data, format='turtle')
    rml_wrapper: RML_Wrapper = RML_Wrapper(rml_graph)

    rml_wrapper.replace_rml_source("resources/llm4rml-movie/diamonds-json/diamonds.json")

    MAPPING_DIRECTORY = 'target/rml/'
    MAPPING_FILE = MAPPING_DIRECTORY+'/'+model_name+'_'+str(idx)+'.rml.ttl' 
    with open(MAPPING_FILE , "w") as f:
        f.write(rml_wrapper.__str__())

    rml_mapper = RMLMapperJavaImpl()
    return rml_mapper.apply_mapping(MAPPING_FILE)

def readOrPass(data_or_file):
    if os.path.exists(data_or_file):
        with open(data_or_file, 'r') as f:
            return f.read()
    else:
        return data_or_file
    
def genRMLStatEntry(output, error, code): 
    resultDict = defaultdict(int)
    resultDict['cnt'] += 1
    if not code == 0 and len(output) > 0:
        resultDict['not_valid_turtle'] += 1
    elif not code == 0:
        resultDict['error_code_not_0'] += 1
    elif code == 0 and len(output) > 0:
        resultDict['valid_turtle'] += 1
    else:
        resultDict['error_code_0_empty_output'] += 1

    return resultDict

def test_generate_stats():
    results = mongo.getAll(FINAL_COLLECTION)
    # copy code from graphische oberfläche

    mongo.drop(FINAL_EVALUATION)

    parsable_results = []
    for result in results:
        if result['meta']['misc']['valid_rdf'] == True:
            parsable_results.append(result)

    with open('resources/llm4rml-movie/diamonds-json/diamonds-reference.ttl', 'r') as f:
        reference_data = f.read()
    reference_graph = Graph()
    reference_graph.parse(data=readOrPass(reference_data), format='turtle')

    cnt = 0 

    all_property_stats = []
    all_additional_stats = []
    all_rml_stats = []
    for idx, parsable_result in enumerate(parsable_results):
        model_name = parsable_result['meta']['model']
        if cnt > -1:
            completion = parsable_result['completion']['message']
            extracted_data = CodeBlockExtractor().extract_codeblocks_from_markdown(completion)
            tr = TurtleRepair(extracted_data)
            tr.repair_prefixes()
            rml_data: Graph = RML_Wrapper(Graph().parse(data=tr.getData(), format="turtle"))
            mapped_result = execute_mapping(idx, model_name, rml_data.__str__(),'final-inception.json')
            # print(f'### {cnt}')
            # print('error_msg_len', str(len(mapped_result['error'])))
            # print('return_code',str(mapped_result['code']))
            # print('output_len', str(len(mapped_result['output'])))
            rml_stat = genRMLStatEntry(mapped_result['output'], mapped_result['error'], mapped_result['code'])
            rml_stat.update({'model': model_name})
            all_rml_stats.append(rml_stat)
        if mapped_result['code'] == 0 and len(mapped_result['output']) > 0:
            with open('target/generated_triples/'+model_name+'_'+str(idx)+'.ttl', 'w') as f:
                f.write(mapped_result['output'])
            test_graph = Graph()
            test_graph.parse(data=mapped_result['output'], format="turtle")
            stats = RML_Evaluation(test_graph, reference_graph).createStatistics()
            stats.update({'_id': parsable_result['_id'], 'model': model_name})

            addStats = RML_Evaluation(test_graph, reference_graph).additionalStats()
            addStats.update({'model': model_name})
            all_additional_stats.append(addStats)

            propertyStats = RML_Evaluation(test_graph, reference_graph).magnifiedPredicatesStats()
            propertyStats.update({'model': model_name})
            all_property_stats.append(propertyStats)
            # print(stats)from bson import json_util
            mongo.update(FINAL_EVALUATION, stats,True)
        
        cnt+=1

    # aggregate rml stats
    rml_statsByModel = defaultdict(lambda: defaultdict(int))
    for rml_stat in all_rml_stats:
        model_name = rml_stat['model']
        for k,v in rml_stat.items():
            if isinstance(v, int):
                rml_statsByModel[model_name][k] += v


    # aggregate additional stats
    additional_statsByModel = defaultdict(lambda: list())
    for additional_stat in all_additional_stats:
        model_name = additional_stat['model']
        additional_statsByModel[model_name].append(additional_stat)

    df_claude = pd.DataFrame(additional_statsByModel['claude-3-opus-20240229'])
    df_claude.to_csv('additional_stats_claude3.csv')
    df_gpt = pd.DataFrame(additional_statsByModel['gpt-4-0125-preview'])
    df_gpt.to_csv('additional_stats_gpt4.csv')

    property_statsByModel = defaultdict(lambda: list())
    for property_stat in all_property_stats:
        model_name = property_stat['model']
        for proper in property_stat.keys():
            if str(proper) == 'model':
                pass
            else:
                sks = property_stat[proper].keys()
                propertry_name = str(proper).split('/')[-1]
                if proper == "http://dbpedia.org/ontology/Work/runtime":
                    propertry_name = "Work/runtime"
                row_data = {}
                row_data["property"] = propertry_name
                for sk in sks:
                    row_data[sk] = property_stat[proper][sk]
                property_statsByModel[model_name].append(row_data)

    for model_name in property_statsByModel.keys():
        rows = property_statsByModel[model_name]
        df_model = pd.DataFrame(rows)
        # df_model.to_csv('property_stats_'+model_name+'.csv')
        df_model_grouped = df_model.groupby('property').sum()
        df_model_grouped.to_csv('property_stats_'+model_name+'.csv')


    # df_claude = pd.DataFrame(property_statsByModel['claude-3-opus-20240229'])
    # df_claude.to_csv('property_stats_claude3.csv')
    # df_gpt = pd.DataFrame(property_statsByModel['gpt-4-0125-preview'])
    # df_gpt.to_csv('property_stats_gpt4.csv')

    print(json.dumps(rml_statsByModel, indent=2))


    # TODO draw stuff

    # print('VALID_RESULTS', len(valid_results))

def test_generate_csv():
    results = list(mongo.getAll(FINAL_EVALUATION))

    print('len', len(results))

    csv_data = []

    exclude_keys = ['_id', 'model', 'classes']

    sub_cnt = 0

    for result in results:
        row = {}
        row.update({'id': result['_id'], 'model': result['model']})
        for k,v in result.items():
            if k not in exclude_keys:
                if k == 'subjects':
                    sub_cnt += 1
                pos_v = v.get('f1', None)
                if not pos_v == None:
                    row.update({k: pos_v})
                    
        csv_data.append(row)


    pd.DataFrame(csv_data).to_csv('stats.csv')

    # with open('stats.csv', 'w') as f:
    #     writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
    #     writer.writeheader()
    #     writer.writerows(csv_data)

def test_generate_figures():
    pass

def test_dump_stats_to_json():
    res = list(mongo.getAll(FINAL_EVALUATION))

    # dump as json lines
    with open('final_stats.json', 'w') as f:
        for r in res:
            f.write(json_util.dumps(r) + '\n')