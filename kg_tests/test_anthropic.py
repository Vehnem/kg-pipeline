### Test Anthropic Claude API reuqests ###

import anthropic
from kg_core import config
from kg_core.llm.anthropic import AnthropicModel
# from anthropic.resources.messages import 

config = config.Config()

def test_anthropic_completion():
    """tests the instruct api"""
    anthropic_model = AnthropicModel(config.ANTHROPIC_API_KEY, 'claude-3-opus-20240229')
    response = anthropic_model.generate("Say this is a test")
    print(response)
    print(anthropic_model.unwrap_response(response))