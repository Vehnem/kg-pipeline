from kg_core.llm.model import Model
import vertexai
from vertexai.generative_models import GenerativeModel, Part


class GeminiModel(Model):

    def __init__(self, config, model_name):
        self.config = config#
        self.model_name = model_name
        vertexai.init(project=config.GCLOUD_PROJECT_ID, location=config.GCLOUD_PROJECT_LOCATION)

    def generate(self, prompt, **kwargs):
        model = GenerativeModel(self.model_name)
        response = model.generate_content(
            [
                prompt
            ]
        )
        return response

    def unwrap_response(self, response):
        return response.text

    def unwrap_usage(self, response):
        usage = response._raw_response.usage_metadata
        return {'total_tokens': usage.total_token_count, 'prompt_tokens': usage.prompt_token_count, 'completion_tokens': usage.candidates_token_count}