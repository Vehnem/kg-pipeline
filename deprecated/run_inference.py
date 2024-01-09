### Mapping Inference ###

import os
from langchain.llms.openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


OPENAI_API_KEY=""

def getMatcherChain() -> LLMChain:
    """
    main method
    """

    template = """Find matches between Ontology A and Ontology B. Answer only with potential matching pairs.

    ### Ontology A
    ```
    {ontologyA}
    ```
    
    ### Ontology B
    ```
    {ontologyB}
    ```
    """
    
    prompt = PromptTemplate(template=template, input_variables=["ontologyA","ontologyB"])

    llm = OpenAI(
        openai_api_key=OPENAI_API_KEY,
        model="gpt-3.5-turbo-instruct",
        temperature=0,
    )

    return LLMChain(prompt=prompt, llm=llm)


matcher = getMatcherChain()
res = matcher.predict(
    ontologyB="""<http://xmlns.com/foaf/0.1/Person> a owl:Class .""",
    ontologyA="""<http://dbpedia.org/ontology/Person> a owl:Class .
    <http://dbpedia.org/ontology/Place> a owl:Class ."""
)

print(res)
