###OpenAI Model###

import openai
from kg_core.llm.model import Model

CHAT_COMPLETION_TYPE = 0
COMPLETION_TYPE = 1

model_map = {
    "gpt-3.5-turbo-instruct" : COMPLETION_TYPE,
    "gpt-3.5-turbo" : CHAT_COMPLETION_TYPE,
    "gpt-4": CHAT_COMPLETION_TYPE,
    "gpt-4-0125-preview": CHAT_COMPLETION_TYPE
}

class OpenAIModel(Model):
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model_name = model_name

    def generate(self, prompt, **kwargs):
        if(model_map[self.model_name] == CHAT_COMPLETION_TYPE):
            openai.api_key = self.api_key
            response = openai.chat.completions.create(
                model = self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                **kwargs
            )
            return response
        else:
            openai.api_key = self.api_key
            response = openai.completions.create(
                model = self.model_name,
                prompt = prompt,
                **kwargs
            )
            return response
        
    def unwrap_response(self, response) -> str:
        return response.choices[0].message.content
    

    def unwrap_usage(self, response):
        return {}