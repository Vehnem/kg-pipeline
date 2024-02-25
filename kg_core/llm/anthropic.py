from llm4kg_core.llm.model import Model
from anthropic import Anthropic

# https://docs.anthropic.com/claude/reference/selecting-a-model

class AnthropicModel(Model):

    def __init__(self, config: dict):
        self.config = config
        self.client = Anthropic(
            api_key=config['api-key']
        )
        pass

    def generate(self, prompt, **kwargs):
        message = self.client.messages.create(
            model="claude-2.1",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            **kwargs
        )
        return message.content