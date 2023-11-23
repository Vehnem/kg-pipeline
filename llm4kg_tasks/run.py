###Entrypoint.###

from llm4kg_tasks.prompts import prompts_util

def run():
    """
    Entry pont method
    """
    prompts_util.matching_prompt("This is A", "This is B")
