### Test Anthropic Claude API reuqests ###

import anthropic
from kg_core import config
from kg_core.llm.anthropic import AnthropicModel
# from anthropic.resources.messages import 


def test_anthropic_completion():
    """tests the instruct api"""
    anthropic_model = AnthropicModel({'api-key': config.ANTHROPIC_API_KEY})
    response = anthropic_model.generate("Say this is a test")
    print(response[0].text)