###Prompt Utils###

import json
from langchain.prompts import PromptTemplate


def matching_prompt(serial_a: str, serial_b: str) -> None:
    """
    Entity Matching Prompt
    """
    prompt = PromptTemplate.from_template(
        "What is a good name for a company that makes {serialA} {serialB}?"
        )
    prompt.format(serialA=serial_a, serialB=serial_b)
    print(json.dumps(prompt.to_json()))
