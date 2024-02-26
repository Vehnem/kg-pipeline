### Test OpenAI API requests ###
from kg_core.config import Config
from kg_core.llm.oai import OpenAIModel

config = Config()

def test_instruct_completion():
    """tests the instruct api"""
    oaim = OpenAIModel({'api-key': config.OPENAI_API_KEY, 'model': 'gpt-3.5-turbo-instruct'})
    response = oaim.generate("Say this is a test")
    print(response)

def test_chat_completion():
    """tests the chat completion api"""
    oaim = OpenAIModel({'api-key': config.OPENAI_API_KEY, 'model': 'gpt-3.5-turbo'})
    response = oaim.generate("Say this is a test", max_tokens=1)
    print(response)

