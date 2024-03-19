###API connector for the lama cpp server."""

import os
from kg_core.llm.model import Model
from kg_core.utils.annotation import todo

@todo
class LlamaCppModel(Model):

    def __init__(self, config: dict):
        pass

    def generate(self, prompt, **kwargs):
        pass

    def unwrap_response(self, response):
        pass

# # https://github.com/langchain-ai/langchain/issues/10415#issuecomment-1720879489

# os.environ[
#         "OPENAI_API_KEY"
#     ] = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # can be anything
# os.environ["OPENAI_API_BASE"] = "http://localhost:8000/v1"
# os.environ["OPENAI_API_HOST"] = "http://localhost:8000"


# # "<s>[INST] {prompt} [/INST]"

# llm = OpenAI(
#     model="gpt-3.5-turbo-instruct",  # can be anything indeed
#     temperature=0,
#     openai_api_base="http://localhost:8000/v1",
#     max_tokens=256,
#     # top_p=1,s
#     # model_kwargs=dict(
#     #     openai_key="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
#     #     top_k=top_k,
#     # ),
#     # presence_penalty=0.0,
#     # n=1,
#     # best_of=1,
#     # batch_size=20,
#     # logit_bias={},
#     # streaming=False
# )

# print(llm.predict("What is Berlin?"))