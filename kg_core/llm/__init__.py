from kg_core.config import Config
from kg_core.llm.google import GeminiModel
from kg_core.llm.oai import OpenAIModel
from kg_core.llm.anthropic import AnthropicModel
from kg_core.llm.model import TestModel

config = Config()

def get_model(model_name):
    llm_models = config.llm_models()
    llm_model = llm_models.get(model_name,None)

    if not llm_model:
        return None
    else:
        if llm_model['class'] == "OpenAIModel":
            return OpenAIModel(config.OPENAI_API_KEY, model_name)
        elif llm_model['class'] == "AnthropicModel":
            return AnthropicModel(config.ANTHROPIC_API_KEY, model_name)
        elif llm_model['class'] == "GoogleModel":
            return GeminiModel(config, model_name)
        elif llm_model['class'] == "TestModel":
            return TestModel(config)
 
def get_model_type(model_name):
    llm_models = config.llm_models()
    llm_model = llm_models.get(model_name,None)

    if not llm_model:
        return None
    else:
        return llm_model['class']