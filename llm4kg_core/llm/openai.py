### OpenAI API connector ###

from openai import openai

class OpenAIAPIConnector:
    """
    Connects to the OpenAI API and generates RML mappings for a given CSV snippet
    """

    __config__ = None

    def __init__(self,config):
        self.__config__ = config

    def completion(self, prompt):
        if self.__config__.model_name == "gpt-3.5-turbo-instruct":
            return self.__chat_completion__(prompt)
        else:
            return self.__completion__(prompt)


    def __chat_completion__(self, prompt):
        response = self.__config__.model.create(
            prompt=prompt,
            max_tokens=2048,
            temperature=0,
            n=1,
            stop=None,
            timeout=5
        )
        # todo fix
        return response.choices[0].text.strip()
    
    def __completion__(self, prompt):
        response = self.__config__.model.create(
            prompt=prompt,
            max_tokens=2048,
            temperature=0,
            n=1,
            stop=None,
            timeout=5
        )
        # todo fix
        return response.choices[0].text.strip()
    

    # def generate_rml_mappings(self, csv_snippet):
    #     # Preprocess the CSV snippet if necessary
        
    #     # Generate RML mappings using OpenAI GPT model
    #     prompt = f"Generate an RML turtle file for the given ontology and CSV snippet:\n\n{csv_snippet}"
    #     response = openai.Completion.create(model="gpt-3.5-turbo-instruct",
    #         prompt=prompt,
    #         max_tokens=2048,
    #         temperature=0,
    #         n=1,
    #         stop=None,
    #         timeout=5
    #     )
        
    #     # Extract the generated RML mappings from the response
    #     rml_mappings = response.choices[0].text.strip()
        
    #     return rml_mappings
    
    # def test(self):
    #     data = """