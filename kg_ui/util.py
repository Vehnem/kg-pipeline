from kg_core.llm.prompt import read_prompt_templates
from kg_core.llm.anthropic  import AnthropicModel, DEFAULT_PARAMETERS
from kg_core.config import Config
from kg_core.utils.cache import MongoCache, CacheDecorator
from kg_core.utils.mongodb import MongoConnection
from kg_core.utils.provenance import MongoProvenance
from kg_core.utils.output_parser import CodeBlockExtractor
from kg_tasks.map.rml_util import RML_Wrapper
from kg_tasks.map.rml_mapper import RMLMapperJavaImpl
from kg_core.llm import get_model, get_model_type
from kg_core.utils.journal import build_llmEntry_v1
from kg_core.metrics.metrics import precision_score
from kg_core.utils.annotation import todo
from kg_core.metrics.metrics import RML_Evaluation
from bson.objectid import ObjectId
from rdflib import Graph, Literal
import anthropic, time, os

cacheImpl = MongoCache('mongodb://localhost:10000/')
cache = CacheDecorator(cacheImpl)
prove = MongoProvenance()

conf = Config()
mongo = MongoConnection(mongo_uri=conf.journal_db_url())
def projects():
    return sorted(list(set(["_".join(collection.split('_')[1:None]) for collection in mongo.list_collections() if collection.startswith('journal_')])))

JOURNAL_COLLECTION = 'journal'
EVALUATION_COLLECTION = 'evaluation'

# @cache.cached
def complete(prompt_message, model_name, prompt_id, prev_hash=None, prompt_vars=dict):
    model = get_model(model_name)

    params = {}
    if get_model_type == 'AnthropicModel':
        params = DEFAULT_PARAMETERS
    elif get_model_type == 'OpenAIModel':
        params = {}
    else:
        pass

    response = model.generate(prompt=prompt_message, **params)
    completion_message = model.unwrap_response(response)

    journalEntry = build_llmEntry_v1(model_name, prompt_message, completion_message, params, prompt_id,prompt_vars,prev_hash).get()
    mongo.insert(journalEntry)
    return journalEntry

def get_all_results(collection_name):
    return list(mongo.getAll(collection_name))
    
def build_prompt(snippet_id, prompt_id):
    with open("kg_tests/resources/llm4rml/rml-ontology_parsed.ttl", "r") as f:
        rml_ontology = f.read()

    with open("kg_tests/resources/llm4rml/target_ontology_parsed.ttl", "r") as f:
        target_ontology = f.read()

    SNIPPET_DIRECTORY = 'target/data_snippets/'
    with open(SNIPPET_DIRECTORY+snippet_id, "r") as f:
        input_data = f.read()

    pt = read_prompt_templates('kg_tests/resources/llm4rml/prompts-rml.yaml')[prompt_id]

    prompt = pt.build({
        # 'RML-ONTO': rml_ontology,
        'TGT-ONTO': target_ontology,
        'DATA' : input_data
    })
    return prompt


def getModel(dict):
    model_name = dict.get('model', None)
    if model_name:
        return model_name
    else:
        return dict['meta']['model']


def execute_repair_instruction(model_name, prompt_id, data, prev_hash) -> str:

    # SNIPPET_DIRECTORY = 'target/data_snippets/'
    # with open(SNIPPET_DIRECTORY+snippet_id, "r") as f:
    #     input_data = f.read()
    
    expecionMessage = None
    try: 
        Graph().parse(data=data, format='turtle')
    except Exception as e:
        expecionMessage = e

    pt = read_prompt_templates('kg_tests/resources/llm4rml/prompts-rml.yaml')[prompt_id]

    prompt = pt.build({
        'DATA': data,
        'MESSAGE': str(expecionMessage)
    })

    completed = complete(prompt, model_name, prompt_id, prev_hash, prompt_vars={'DATA': None, 'MESSAGE': None})

    return completed


def execute_instruction(model_name, snippet_id, prompt_id) -> str:
    with open("kg_tests/resources/llm4rml/rml-ontology_parsed.ttl", "r") as f:
        rml_ontology = f.read()

    ONTOLOGY_FILE = 'kg_tests/resources/llm4rml/target_ontology_parsed.ttl'
    with open(ONTOLOGY_FILE, "r") as f:
        target_ontology = f.read()

    SNIPPET_DIRECTORY = 'target/data_snippets/'
    SNIPPET_FILE = SNIPPET_DIRECTORY+snippet_id
    with open(SNIPPET_FILE, "r") as f:
        input_data = f.read()

    pt = read_prompt_templates('kg_tests/resources/llm4rml/prompts-rml.yaml')[prompt_id]

    prompt = pt.build({
        # 'RML-ONTO': rml_ontology,
        'TGT-ONTO': target_ontology,
        'DATA' : input_data
    })

    completed = complete(prompt, model_name, prompt_id, prompt_vars={'TGT-ONTO': ONTOLOGY_FILE, 'DATA': SNIPPET_FILE})

    prove.set(prompt, completed)

    return completed['completion']['message']
    # TODO no code block found exception
    # return CodeBlockExtractor().extract_codeblocks_from_markdown(completed)

@cache.cached
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

BASE_IRI="http://mykg.org/resource/"

# https://en.wikipedia.org/wiki/Precision_and_recall
def precision_score(tp, fp):
    return tp / (tp + fp) if tp + fp > 0 else 0

def recall_score(tp, fn):
    return tp / (tp + fn) if tp + fn > 0 else 0

def f1_score(tp, fp, fn):
    precision = precision_score(tp, fp)
    recall = recall_score(tp, fn)
    return 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0


def update_doc(doc):
    mongo.update(JOURNAL_COLLECTION,doc)

def insert_eval(doc):
    mongo.update(EVALUATION_COLLECTION, doc, upsert=True)

def remove_eval(id):
    mongo.removeById(EVALUATION_COLLECTION, id)


def getEvaluationStats(collection_name):
    return mongo.getAll(collection_name)


def createStatistics(test_data, reference_data=None) -> dict:
    
    with open('/workspace/papers/llm4rml/kg-pipeline/target/output/gold.ttl', 'r') as f:
        reference_data = f.read()

    test_graph = Graph()
    test_graph.parse(data=readOrPass(test_data), format='turtle')
    reference_graph = Graph()
    reference_graph.parse(data=readOrPass(reference_data), format='turtle')


    return RML_Evaluation(test_graph, reference_graph).createStatistics()