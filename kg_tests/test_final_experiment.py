from kg_core.llm import get_model
from kg_core.utils.journal import build_llmEntry_v2
from kg_core.utils.mongodb import MongoConnection
from kg_core.utils.output_parser import CodeBlockExtractor
from kg_core.llm.prompt import read_prompt_templates
from kg_core.config import Config
from kg_core.utils.mongodb import MongoConnection
from kg_core.utils.output_parser import CodeBlockExtractor
from kg_tasks.map.rml_mapper import RMLMapperJavaImpl
from kg_tasks.map.rml_util import RML_Wrapper
from kg_core.metrics.metrics import RML_Evaluation
from kg_tasks.repair.rdfrepair import TurtleRepair
from kg_core.utils.log import Logger
from rdflib import Graph
import os, time, datetime

log = Logger("MainTest")

unique_id= datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%S")

config = Config()
mongo = MongoConnection(mongo_uri='mongodb://localhost:10000/')

JOURNAL_COLLECTION="journal_final_claude3"
TEST_JOURNAL_COLLECTION="journal_combined_1"
TEST_EVAL_COLLECTION="evaluation_combined_1"
# 2024_03_04T12_55_14
# 2024_03_01T20_18_50

test_final_dumy_config = {
    'model': 'test-rml',
    'rml_prompt_id' : 'final-rml',
    'snippet_id' : 'resources/llm4rml-movie/diamonds-json/diamonds.json',
    'turtle_repair_prompt' : 'final-repair',
    'iterations' : 4,
    'parameters': {},
    'delay': 0
}

test_final_config_gpt35 = {
    'model': 'gpt-3.5-turbo',
    'rml_prompt_id' : 'final-rml',
    'snippet_id' : 'resources/llm4rml-movie/diamonds-json/diamonds.json',
    'turtle_repair_prompt' : 'final-repair',
    'iterations' : 40,
    'parameters': {},
    'delay': 15
}

test_final_config_gpt4 = {
    'model': 'gpt-4',
    'rml_prompt_id' : 'final-rml',
    'snippet_id' : 'final-inception.json',
    'turtle_repair_prompt' : 'final-repair',
    'iterations' : 20,
    'parameters': {}
}

test_final_config_claude21_t0 = {
    'model': 'claude-2.1',
    'rml_prompt_id' : 'final-rml',
    'snippet_id' : 'inception-01.json',
    'turtle_repair_prompt' : 'final-repair',
    'iterations' : 10,
    'parameters': {
        'temperature': 0
    }
}

test_final_config_claude3opus = {
    'model': 'claude-3-opus-20240229',
    'rml_prompt_id' : 'final-rml',
    'snippet_id' : 'resources/llm4rml-movie/diamonds-json/diamonds.json',
    'turtle_repair_prompt' : 'final-repair',
    'iterations' : 40,
    'parameters': {},
    'delay': 20
}

test_final_config_gemini_pro= {
    'model': 'gemini-pro',
    'rml_prompt_id' : 'final-rml',
    'snippet_id' : 'resources/llm4rml-movie/diamonds-json/diamonds.json',
    'turtle_repair_prompt' : 'final-repair',
    'iterations' : 40,
    'parameters': {},
    'delay': 20
}

test_conf = test_final_config_claude3opus


def load_rml_prompt(rml_prompt_id):
    return read_prompt_templates('kg_tests/resources/llm4rml/prompts-rml.yaml')[rml_prompt_id]

def load_data(file):
    with open(file, 'r') as f:
        return f.read()

DEFAULT_RML=load_data('target/test/test.rml.ttl')
DEFAULT_RML_BROKEN=load_data('target/test/test_broken.rml.ttl')
DEFAULT_RML_BROKEN_PREFIX=load_data('target/test/test_broken_prefix.rml.ttl')

START_PROMPTS=[DEFAULT_RML, DEFAULT_RML_BROKEN,DEFAULT_RML_BROKEN_PREFIX]

def validate_rdf(data, format="turtle"):
    graph = Graph()
    try :
        graph.parse(data=data, format=format)
        return None
    except Exception as e:
        return str(e)


def insert_in_test_journal(entry):
    mongo.insert(JOURNAL_COLLECTION, entry)

def do_iteration(iteration, test_conf, RML_PROMPT, REPAIR_PROMPT_TEMPLATE):

    journal_entries = []

    model = get_model(test_conf['model'])
    # response = model.generate(RML_PROMPT,**test_conf['parameters'], default=START_PROMPTS[iteration%3])
    response = model.generate(RML_PROMPT,**test_conf['parameters'])
    completion = model.unwrap_response(response)
    log.debug(model.unwrap_usage(response))
    extracted_data = CodeBlockExtractor().extract_codeblocks_from_markdown(completion)
    tr = TurtleRepair(extracted_data)
    tr.repair_prefixes()
    parsing_error = validate_rdf(tr.getData(), format="turtle")

    journal_entry = build_llmEntry_v2(
        model=test_conf['model'], 
        prompt=RML_PROMPT, 
        completion=completion, 
        parameters=test_conf['parameters'], 
        prompt_id=test_conf['rml_prompt_id'], 
        prompt_vars={'TGT-ONTO':config.ONTOLOGY_FILE,'DATA': config.SNIPPET_DIR+test_conf['snippet_id']}, 
        prev_hash=None,
        misc={'valid_rdf': True if not parsing_error else False}).get()


    journal_entries.append(journal_entry)
    
    repairs = 0
    while (parsing_error and repairs <2):
        log.debug(f"waiting {test_conf['delay']}s before next request")
        time.sleep(test_conf['delay'])

        # TODO try repair 2 times
        log.info(f'iteration {iteration} @ repair {repairs+1}')
        repair_prompt = REPAIR_PROMPT_TEMPLATE.build({
            'DATA': extracted_data,
            'MESSAGE': parsing_error
        })
        # response = model.generate(repair_prompt, **test_conf['parameters'], default=DEFAULT_RML)
        response = model.generate(repair_prompt, **test_conf['parameters'])
        completion = model.unwrap_response(response)
        log.debug(model.unwrap_usage(response))
        extracted_data = CodeBlockExtractor().extract_codeblocks_from_markdown(completion)
        tr = TurtleRepair(extracted_data)
        tr.repair_prefixes()
        parsing_error = validate_rdf(tr.getData(), format="turtle")

        # SAVE
        journal_entry = build_llmEntry_v2(
            model=test_conf['model'], 
            prompt=repair_prompt, 
            completion=completion, 
            parameters=test_conf['parameters'], 
            prompt_id=test_conf['turtle_repair_prompt'], 
            prompt_vars={'DATA': '', 'MESSAGE': ''}, 
            prev_hash=journal_entry['hash'],
            misc = {'valid_rdf': True if not parsing_error else False}).get()

        journal_entries.append(journal_entry)
        
        repairs += 1

    
    for journal_entry in journal_entries:
        mongo.insert(JOURNAL_COLLECTION, journal_entry)

def test_final_dumy():
    print('unique_id', unique_id)
    print('test_conf', test_conf)

    RML_PROMPT_TEMPLATE = load_rml_prompt(test_conf['rml_prompt_id'])

    DATA = load_data(test_conf['snippet_id'])

    TARGET_ONTOLOGY = load_data("resources/llm4rml-movie/ontology.ttl")

    RML_PROMPT = RML_PROMPT_TEMPLATE.build({
        'DATA': DATA,
        'TGT-ONTO': TARGET_ONTOLOGY
    })

    REPAIR_PROMPT_TEMPLATE = load_rml_prompt(test_conf['turtle_repair_prompt'])

    max_retries = 5
    retries = 0
    iteration = 1
    while iteration <= test_conf['iterations'] and retries <= max_retries:
        if iteration > 1 or retries > 0:
            log.debug(f"waiting {test_conf['delay']}s before next request")
            time.sleep(test_conf['delay'])

        log.info(f"iteration {iteration}")

        try:
            do_iteration(iteration, test_conf, RML_PROMPT, REPAIR_PROMPT_TEMPLATE)
            iteration += 1
        except Exception as e:
            log.error(f"exception in iteration {iteration}: {e}")
            log.info(f"retry of iteration {iteration}")
            retries += 1
            time.sleep(120)
        

def execute_mapping(mapping_data, snippet_id) -> str:

    rml_graph = Graph().parse(data=mapping_data, format='turtle')
    rml_wrapper: RML_Wrapper = RML_Wrapper(rml_graph)

    SNIPPET_DIRECTORY = 'target/data_snippets/'
    rml_wrapper.replace_rml_source(SNIPPET_DIRECTORY+snippet_id)

    MAPPING_DIRECTORY = 'target/rml/'
    MAPPING_FILE = MAPPING_DIRECTORY+'/'+str(int(time.time()))+'.ttl' 
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
    
def test_prepare_eval():
    test_conf=test_final_config_gpt4
    valid_results = []
    for result in list(mongo.getAll(TEST_JOURNAL_COLLECTION)):
        try:
            if result['meta']['misc']['valid_rdf'] == True:
                valid_results.append(result)
        except:
            print(result['meta'])

    with open('/workspace/papers/llm4rml/kg-pipeline/target/output/gold.ttl', 'r') as f:
        reference_data = f.read()
    reference_graph = Graph()
    reference_graph.parse(data=readOrPass(reference_data), format='turtle')

    print('VALID_RESULTS', len(valid_results))
    for result in valid_results:
        print()
        print('###')
        print(result['hash'])
        print(result['_id'])
        print('###')
        completion = result['completion']['message']
        extracted_data = CodeBlockExtractor().extract_codeblocks_from_markdown(completion)

        # print(extracted_data)
        try:
            rml_data: Graph = RML_Wrapper(Graph().parse(data=extracted_data, format="turtle"))
            mapped = execute_mapping(rml_data.__str__(),test_conf['snippet_id'])

            test_graph = Graph()
            test_graph.parse(data=readOrPass(mapped), format='turtle')
            stats = RML_Evaluation(test_graph, reference_graph).createStatistics()
            model_name = result['meta']['model']
            stats.update({'_id': result['_id'], 'model': model_name})
            print(stats)
            mongo.update(TEST_EVAL_COLLECTION, stats,True)
            print('OK')
        except Exception as e:
            print('ERROR', e)
            continue
        # test_graph.parse(data=readOrPass(mapped), format='turtle')



# TODO clean an untangle code

def test_copy_journals():
    # gpt 3 journal_2024_02_28T22_27_12

    # gpt 4 journal_2024_02_28T22_46_10
    # claude 2.1 journal_2024_02_29T00_28_59
    # colls = [ 'journal_2024_02_28T22_27_12', 'journal_2024_02_28T22_46_10', 'journal_2024_02_29T00_28_59']
    colls = ["journal_2024_03_01T15_55_49", "journal_2024_03_04T17_24_17", "journal_2024_03_04T15_47_58"]


    mongo = MongoConnection(mongo_uri='mongodb://localhost:10000/')

    for coll in colls:
        results = list(mongo.getAll(coll))
        for result in results:
            del result['_id']
            mongo.insert("journal_combined_1",result)

def test_claude_output():
        coll_name = "journal_2024_02_29T00_28_59"

        coll = MongoConnection(mongo_uri='mongodb://localhost:10000/', collection_name=coll_name)

        for idx, res in enumerate(list(coll.getAll())):
            isValid = res['meta']['misc']['valid_rdf']
            if(not isValid):
                extracted = CodeBlockExtractor().extract_codeblocks_from_markdown(res['completion']['message'])
                tr = TurtleRepair(extracted)
                print('repaired', tr.is_repaired())
                tr.repair_prefixes()
                print('repaired', tr.is_repaired())
                coll.update(res, True)
            