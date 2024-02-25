from llm4kg_core.llm.prompt import PromptTemplate, read_prompt_templates

def test_prompts():
    prompts = read_prompt_templates('llm4kg_tests/prompts/prompts-rml.yaml')
    print(prompts['current'])