### Test OpenAI API requests ###
import openai
from llm4kg_core import config
from llm4kg_core.llm.oai import OpenAIModel


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

# def test_completion_with_cache():
#     """tests the instruct api"""
#     openai.api_key = config.OPENAI_API_KEY #Your openai API key
#     response = openai.Completion.create(
#         model="gpt-3.5-turbo-instruct",
#         prompt="Say this is a test",
#         temperature=0,
#         max_tokens=7
#     )
#     print(response)


# def test_chat_completion():
#     """tests the chat completion api"""
#     openai.api_key = config.OPENAI_API_KEY
#     response = openai.ChatCompletion.create(
#         model = "gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": "Say this is a test"}
#         ],
#         temperature=0,
#         max_tokens=7
#     )
#     print(response)
