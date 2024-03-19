import yaml, json
from typing import Dict
from schema import Schema, And, Use, Optional, SchemaError

class PromptTemplate:
    """
    Prompt Template Class
    """

    def __init__(self, id, description, prompt, variables):
        self.id = id
        self.description = description
        self.prompt = prompt
        self.variables = variables


    def build(self, input: dict):
        promptBuilder = self.prompt
        for var in self.variables:
            promptBuilder = promptBuilder.replace('{{' + var + '}}', input[var])
        return promptBuilder
    

    def __str__(self) -> str:
        return json.dumps({'id': self.id, 'description': self.description, 'prompt': self.prompt, 'variables': self.variables}, indent=2)


def read_yaml_file(file_path):
    """
    Read and return the contents of a YAML file.
    
    :param file_path: Path to the YAML file
    :return: Parsed YAML content as a dictionary
    """
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def read_prompt_templates(file_path) -> Dict[str, PromptTemplate]: 
    """
    Read and return the contents of the prompt templates YAML file.
    
    :return: Parsed prompt template YAML as List of PrommtTemplate
    """
    prompts_dict = read_yaml_file(file_path)
    prompts: Dict[str, PromptTemplate] = {}
    for prompt in prompts_dict:
        promptTemplate = PromptTemplate(**prompt)
        prompts.update({ prompt['id'] : promptTemplate })

    return prompts

class Prompt():

    

    def __init__(self, id, description, prompt, variables):
        self.id = id
        self.description = description
        self.prompt = prompt
        self.variables = variables