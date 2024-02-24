### Test RML Mapper ###
from llm4kg_tasks.map.rml_mapper import RMLMapperJavaImpl
from rdflib import Graph
from llm4kg_core.llm.prompt import read_prompt_templates
from llm4kg_core.llm.anthropic import AnthropicModel
from llm4kg_core import config
from llm4kg_core.utils.cache import MongoCache, CacheDecorator
from llm4kg_core.utils.output_parser import CodeBlockExtractor
from llm4kg_tasks.map.rml_util import RML_Wrapper

cacheImpl = MongoCache('mongodb://localhost:10000/')
cache = CacheDecorator(cacheImpl)

def test_replace_source():
    # rml_data = RML_Wrapper()
    # rml_data.replace_data_source("someSource")
    pass

@cache.cached
def __send_request(prompt: str):
    model = AnthropicModel({'api-key': config.ANTHROPIC_API_KEY})
    response = model.generate(prompt=prompt,  max_tokens=4096)
    return response[0].text


def test_rml_final():
    # rml_ontology = Graph()
    # rml_ontology.parse("data/rml-ontology/rml-ontology-core.ttl", format="turtle")
    # rml_ontology.parse("data/rml-ontology/rml-ontology-module-input-output-sources-targets.ttl", format="turtle")
    # rml_ontology.parse("data/rml-ontology/rml-ontology-module-collections-containers.ttl", format="turtle")
    # rml_ontology.parse("data/rml-ontology/rml-ontology-module-transformation-functions.ttl", format="turtle")
    # rml_ontology.serialize(destination="data/rml-ontology_parsed.ttl", format="turtle")

    # target_ontology = Graph()
    # target_ontology.parse("data/target_ontology.ttl", format="turtle")
    # target_ontology.serialize(destination="data/target_ontology_parsed.ttl", format="turtle")

    with open("llm4kg_tests/resources/llm4rml/rml-ontology_parsed.ttl", "r") as f:
        rml_ontology = f.read()

    with open("llm4kg_tests/resources/llm4rml/target_ontology_parsed.ttl", "r") as f:
        target_ontology = f.read()

    with open("llm4kg_tests/resources/llm4rml/inception.json", "r") as f:
        input_json = f.read()

    pt = read_prompt_templates('llm4kg_tests/resources/llm4rml/prompts-rml.yaml')['development']

    prompt = pt.build({
        'RML-ONTO': rml_ontology,
        'TGT-ONTO': target_ontology,
        'JSON' : input_json
    })

    response = __send_request(prompt)

    with open("data/prompt.md", "w") as md_file:
        md_file.write(prompt)
        print("wrote prompt to file")

    possible_mapping_data = CodeBlockExtractor().extract_codeblocks_from_markdown(response)

    try:
        possible_mapping_data = RML_Wrapper(possible_mapping_data)
    except:
        # print(possible_mapping_data)
        pass

    # RMLMapperJavaImpl().apply_mapping(
    #     mapping_path=possible_mapping_data,
    #     output_path='test_rml_output.ttl', 
    # )