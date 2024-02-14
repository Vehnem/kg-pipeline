from llm4kg_core.llm.oai import OpenAIModel
from llm4kg_core.utils.cache import MongoCache, CacheDecorator

test_data = [
    {
        'prompt': 'Generate an RML mapping to DBpedia given the following CSV snippet:\n\n'
    },
    {
        'prompt': 'Generate an RML mapping given the following ontology and CSV snippet:\n\n$CSV$',
        'vars': ['csv']
    }
]

cache = CacheDecorator(MongoCache(mongo_uri='mongodb://localhost:10000/'))

model = OpenAIModel({'api-key': "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"}, 'gpt-3.5-turbo-instruct')

### Generate RML 

@cache.cached
def generate_rml_mappings(csv_snippet):
    # Preprocess the CSV snippet if necessary
    
    # Generate RML mappings using OpenAI GPT model
    prompt = f"Generate an RML turtle file for the given ontology and CSV snippet:\n\n{csv_snippet}"
    response = model.generate(prompt)
    return response

csv_snippets=[]

for csv_snippet in test_data:
    print(generate_rml_mappings(csv_snippet['prompt']))

    # def __init__(self, model_name):
    #     openai.api_key = "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" #Your openai API key
    #     self.model = openai.Completion.create(model=model_name)
    #     # Initialize any other required variables
    
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
    
#     def test(self):
#         data = """
# tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres
# tt0120338	movie	Titanic	Titanic	0	1997	NONE	194	Drama,Romance
# """
#         ontology = """

# """


# # OPENA_AI_MODEL = "gpt-3.5-turbo"
# DEFAULT_TEMPERATURE = 1

# OPENA_AI_MODEL = "gpt-3.5-turbo-instruct"

# response = openai.Completion.create(
# model=OPENA_AI_MODEL,
# prompt=prompt,
# temperature=DEFAULT_TEMPERATURE,
# max_tokens=2048,
# n=1,
# stop=None,
# presence_penalty=0,
# frequency_penalty=0.1,
# )

# messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": prompt},
# ]

# response = openai.ChatCompletion.create(
# model=OPENA_AI_MODEL,
# messages=messages,
# temperature=DEFAULT_TEMPERATURE,
# max_tokens=2048,
# n=1,
# stop=None,
# presence_penalty=0,
# frequency_penalty=0.1,
# )   

# print(response)