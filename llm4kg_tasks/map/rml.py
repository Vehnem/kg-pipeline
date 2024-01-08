import openai

class RML:

    model_name = ""

    def __init__(self, model_name):
        openai.api_key = "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" #Your openai API key
        self.model_name = model_name
        # self.model = openai.Completion.create(model=model_name)
        # Initialize any other required variables
    
    def generate_rml_mappings(self, csv_snippet, ontology):
        # Preprocess the CSV snippet if necessary
        
        # Generate RML mappings using OpenAI GPT model
        prompt = f"Generate an RML turtle file for a TSV file and a given ontology. The TSV is located at '/home/example.tsv'\n\nCSV:\n\n{csv_snippet}\n\nOntology:\n\n{ontology}"

        if(self.model_name.endswith("instruct")):
            response = openai.Completion.create(model=self.model_name,
                prompt=prompt,
                max_tokens=2048,
                temperature=0,
                n=1,
                stop=None,
                timeout=5
            )
            # Extract the generated RML mappings from the response
            rml_mappings = response.choices[0].text.strip()
            return rml_mappings
        else:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ]
            response = openai.ChatCompletion.create(model=self.model_name,
                messages=messages,
                max_tokens=2048,
                temperature=0,
                n=1,
                stop=None,
                timeout=5
            )
            # Extract the generated RML mappings from the response
            rml_mappings = response.choices[0].message.content.strip()
            return rml_mappings


# Usage example
rml = RML("gpt-4")
# rml = RML("gpt-3.5-turbo-instruct")

csv_snippet = """
nconst	primaryName	birthYear	deathYear	primaryProfession	knownForTitles
nm0000035	James Horner	1953	2015	music_department,soundtrack,composer	tt0120338,tt0499549,tt0177971,tt0120746
nm0000116	James Cameron	1954	N	writer,producer,director	tt0120338,tt1630029,tt0090605,tt0499549
nm0000138	Leonardo DiCaprio	1974	N	producer,actor,soundtrack	tt0120338,tt0407887,tt1375666,tt0338751
nm0000701	Kate Winslet	1975	N	actress,producer,soundtrack	tt0114388,tt0120338,tt0338013,tt0959337
nm0000708	Billy Zane	1966	N	actor,producer,soundtrack	tt0096874,tt0097162,tt0117331,tt0120338
nm0000751	Suzy Amis	1962	N	actress,producer,soundtrack	tt0106350,tt0114814,tt0120338,tt0109303
nm0000870	Kathy Bates	1948	N	actress,director,soundtrack	tt0257360,tt0100157,tt0120338,tt0109642
nm0000967	Eric Braeden	1941	N	actor,producer	tt0069658,tt0064177,tt0120338,tt0067065
nm0001144	Céline Dion	1968	N	music_artist,soundtrack,actress	tt2281587,tt5463162,tt0101414,tt0120338"""

ontology = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

rdfs:label a rdf:Property ;
    rdfs:label "label"@en .
dbo:Person a owl:Class ;
    rdfs:label "Person"@en .
dbo:birthYear a owl:DatatypeProperty ;
    owl:domain dbo:Person ;
    rdfs:label "birth year"@en .
dbo:deathYear a owl:DatatypeProperty ;
    owl:domain dbo:Person ;
    rdfs:label "death year"@en .
dbo:profession a owl:ObjectProperty ;
    owl:domain dbo:Person ;
    rdfs:label "profession"@en .
dbo:Film a owl:Class ;
    rdfs:label "Film"@en .
dbo:starring a owl:ObjectProperty ;
    owl:domain dbo:Film ;
    rdfs:label "starring"@en .
"""

ontology2="""  
Person(name,birthYear,deathYear,profession)
Film(title,releaseYear,genre,starring)
"""

generated_mappings = rml.generate_rml_mappings(csv_snippet,ontology2)
print(generated_mappings)
