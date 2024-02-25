import openai
###Completion Tasks###

class LLMSynonymCompletion:
    def __init__(self, api_key, model_name):
        openai.api_key = api_key
        self.model_name = model_name

    # TODO new api
    def get_synonyms(self, word):
        response = openai.Completion.create(
            engine=self.model_name,
            prompt=f"Give me synonyms for {word}.",
            max_tokens=50,
            n=10,
            stop=None,
            temperature=0.5,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        synonyms = [choice['text'].strip() for choice in response.choices]
        return synonyms