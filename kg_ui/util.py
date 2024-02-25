from llm4kg_core.llm.prompt import read_prompt_templates
from llm4kg_core.llm.anthropic  import AnthropicModel
from llm4kg_core.config import Config
from llm4kg_core.utils.cache import MongoCache, CacheDecorator
from llm4kg_core.utils.provenance import MongoProvenance
from llm4kg_core.utils.output_parser import CodeBlockExtractor

cacheImpl = MongoCache('mongodb://localhost:10000/')
cache = CacheDecorator(cacheImpl)
prove = MongoProvenance()
conf = Config()

@cache.cached
def complete(prompt):
    model = AnthropicModel({'api-key': conf.ANTHROPIC_API_KEY})
    response = model.generate(prompt=prompt,  max_tokens=4096)
    return response[0].text

def execute_instruction(snippet_id, prompt_id) -> str:
    with open("/workspace/papers/llm4rml/kg-pipeline/llm4kg_tests/resources/llm4rml/rml-ontology_parsed.ttl", "r") as f:
        rml_ontology = f.read()

    with open("/workspace/papers/llm4rml/kg-pipeline/llm4kg_tests/resources/llm4rml/target_ontology_parsed.ttl", "r") as f:
        target_ontology = f.read()

    SNIPPET_DIRECTORY = '/workspace/papers/llm4rml/kg-pipeline/target/data_snippets/'
    with open(SNIPPET_DIRECTORY+snippet_id, "r") as f:
        input_data = f.read()

    pt = read_prompt_templates('llm4kg_tests/resources/llm4rml/prompts-rml.yaml')[prompt_id]

    prompt = pt.build({
        'RML-ONTO': rml_ontology,
        'TGT-ONTO': target_ontology,
        'JSON' : input_data
    })

    completed = complete(prompt)

    prove.set(prompt, completed)

    return completed
    # TODO no code block found exception
    # return CodeBlockExtractor().extract_codeblocks_from_markdown(completed)
