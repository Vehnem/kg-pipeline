### OpenAI API connector ###

import openai
from kg_core.llm.model import Model

CHAT_COMPLETION_TYPE = 0
COMPLETION_TYPE = 1

model_map = {
    "gpt-3.5-turbo-instruct" : COMPLETION_TYPE,
    "gpt-3.5-turbo" : CHAT_COMPLETION_TYPE
}

class OpenAIModel(Model):
    def __init__(self, config: dict):
        self.config = config

    def generate(self, prompt, **kwargs):
        if(model_map[self.config['model']] == CHAT_COMPLETION_TYPE):
            openai.api_key = self.config['api-key']
            response = openai.ChatCompletion.create(
                model = self.config['model'],
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response
        else:
            openai.api_key = self.config['api-key']
            response = openai.Completion.create(
                model = self.config['model'],
                **kwargs
            )
            return response
        

    