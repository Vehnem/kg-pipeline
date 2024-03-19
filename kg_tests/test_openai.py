### Test OpenAI API requests ###
from kg_core.config import Config
from kg_core.llm import get_model

config = Config()

# def test_instruct_completion():
#     """tests the instruct api"""
#     model = get_model('gpt-3.5-turbo-instruct')
#     response = model.generate("Say this is a test")
#     print(response)

def test_chat_completion():
    """tests the chat completion api"""
    model = get_model('gpt-4-0125-preview')
    response = model.generate("Say this is a test")
    print(response.usage.total_tokens)

