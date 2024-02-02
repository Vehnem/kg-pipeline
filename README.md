# Data Integration & Knowledge Graphs

**Summary**
- 

**Structure**
- **llm4kg_core** - core components of the framework
- **llm4kg_tasks** - boilerplate code to modularize exisiting construction tools
- **llm4kg_bench** - benchmarking suite for the construction process

What do I need
- M1: I need to generate the example benchmark data from Wikipedia, DBpedia, Wikidata, IMDB
- M2: I need to write prompts for the tasks
- M3: I need to write an API to execute the tasks


# Milestone 1

- get all possible raw data and store on a server

IMDB

- generate samples for coding



https://platform.openai.com/docs/models

## Slefhost APIs
https://github.com/marella/ctransformers
https://github.com/abetlen/llama-cpp-python is very good

## Python-LLAMMA-cpp is working good

## Datasets

sudo apt install libcurl4-openssl-dev libssl-dev


## Backlog


- what is the prompt format of GPT4
- what kinds of LLMs should be used
- use of unit testing with poerty
- use of `typer` for commandline stuff
- use of `langchain`, maybe watch youtube video
- configure prompts in YAML file
- profile memory usage. Use WeightsAndBiases or https://www.pluralsight.com/blog/tutorials/how-to-profile-memory-usage-in-python

https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
https://github.com/abetlen/llama-cpp-python/pkgs/container/llama-cpp-python
https://huggingface.co/docs/transformers/training#train
https://github.com/ChuloAI/BrainChulo
- finetuning with python

## Prompts
- Lets think Step by Step

```
Summary of the task

Question:
Answer:
Question:
```

Prompt Formats


## Tools

https://github.com/srush/MiniChain

## How To's

https://cobusgreyling.medium.com/langchain-creating-large-language-model-llm-applications-via-huggingface-192423883a74


## Open LLMs 

https://github.com/antimatter15/alpaca.cpp

https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard

## Related Work/Repos ##

https://github.com/HazyResearch/fm_data_tasks

https://aclanthology.org/2023.bionlp-1.37/

## Logs

```
# Testing ZephyrB Alpha 7B with CPU only no accel

(venv) marvin@XPS15:~/src/llm4kg$ /home/marvin/.pyenv/versions/3.10.13/envs/venv/bin/python /home/marvin/src/llm4kg/llm4kg_mapping/transformers_test.py
Loading checkpoint shards: 100%|███████████████████████████████████████████████████████████████████████████████████| 8/8 [06:44<00:00, 50.55s/it]
Special tokens have been added in the vocabulary, make sure the associated word embeddings are fine-tuned or trained.
pipeline =  517.6861371994019
Using sep_token, but it is not set yet.
Using cls_token, but it is not set yet.
Using mask_token, but it is not set yet.
/home/marvin/.pyenv/versions/3.10.13/envs/venv/lib/python3.10/site-packages/transformers/generation/utils.py:1421: UserWarning: You have modified the pretrained model configuration to control generation. This is a deprecated strategy to control generation and will be removed soon, in a future version. Please use and modify the model generation configuration (see https://huggingface.co/docs/transformers/generation_strategies#default-text-generation-configuration )
  warnings.warn(
[{'generated_text': "<|system|>\nYou are a friendly chatbot who always responds in the style of a pirate</s>\n<|user|>\nHow many helicopters can a human eat in one sitting?</s>\n<|assistant|>\nAhoy matey! There be no way a human can eat a helicopter, 'tis an impossible feat! A human can't even eat a helicopter's parts, as they are mainly made of metal and other materials that cannot be digested. I reckon you be confusing helicopters with helicopter food, like cheese and crackers or fruit and nuts. Yo ho ho!"}]
inference =  1228.7278909683228
```

```
"""
"Given the following descriptions of two entities, determine if they refer to the same thing. Provide a confidence score or reasoning for your decision.

Entity 1:

Name: [Name]
Description: [Description]
Location: [Location]
Established: [Year]
[Any other relevant attribute]

Entity 2:

Name: [Name]
Description: [Description]
Location: [Location]
Established: [Year]
[Any other relevant attribute]

Please analyze the information provided for Entity 1 and Entity 2, cross-reference the attributes, and state whether they are the same. If they match, specify which attributes contributed most to your conclusion. If they do not, identify the attributes that show the most significant differences."""

"""
Entity Matching Task:

Determine if the entities described below represent the same real-world object or individual. Provide a justification for your decision based on the similarities or differences in their attributes.

Entity 1:

Name: [Name]
Type/Category: [Type/Category]
Location: [Location]
Attribute 1: [Value]
Attribute 2: [Value]
...
Attribute N: [Value]
Entity 2:

Name: [Name]
Type/Category: [Type/Category]
Location: [Location]
Attribute 1: [Value]
Attribute 2: [Value]
...
Attribute N: [Value]
Please analyze the attributes of both entities and identify whether they refer to the same thing. Highlight the key attributes that informed your decision.

"""
```

## Output Experiments

## Tasks

### Entity Matcher

## Entiy 2 Entity Matcher

```
@prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix ql: <http://semweb.mmlab.be/ns/ql#> .
@prefix rml: <http://semweb.mmlab.be/ns/rml#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

<#MusicDepartmentsMapping>
  rr:logicalTable [
    rr:tableName "CSVSnippet"
  ];
  rr:subjectMap [
    rr:template "http://musicproject.com/artist/{nconst}"
  ];
  rr:predicateObjectMap [
    rr:predicate rr:primaryName;
    rr:objectMap [ rr:column "primaryName" ]
  ];
  rr:predicateObjectMap [
    rr:predicate rr:birthYear;
    rr:objectMap [ rr:column "birthYear" ]
  ];
  rr:predicateObjectMap [
    rr:predicate rr:deathYear;
    rr:objectMap [ rr:column "deathYear" ]
  ];
  rr:predicateObjectMap [
    rr:predicate rr:primaryProfession;
    rr:objectMap [ rr:column "primaryProfession" ]
  ];
  rr:predicateObjectMap [
    rr:predicate rr:knowForTitles;
    rr:objectMap [ rr:column "knownForTitles" ]
  ].```


  Temp=0
  ```
  @prefix rr: <http://www.w3.org/ns/r2rml#> .
@prefix rml: <http://semweb.mmlab.be/ns/rml#> .
@prefix ql: <http://semweb.mmlab.be/ns/ql#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ex: <http://example.com/> .

ex:MappingTriplesMap
    a rr:TriplesMap;
    rr:logicalTable [
        rr:tableName "CSVSnippet";
    ];
    rr:subjectMap [
        rr:template "http://example.com/{nconst}";
        rr:class ex:Person;
    ];
    rr:predicateObjectMap [
        rr:predicate ex:primaryName;
        rr:objectMap [
            rml:reference "primaryName";
        ];
    ];
    rr:predicateObjectMap [
        rr:predicate ex:birthYear;
        rr:objectMap [
            rml:reference "birthYear";
            rr:datatype xsd:integer;
        ];
    ];
    rr:predicateObjectMap [
        rr:predicate ex:deathYear;
        rr:objectMap [
            rml:reference "deathYear";
            rr:datatype xsd:integer;
        ];
    ];
    rr:predicateObjectMap [
        rr:predicate ex:primaryProfession;
        rr:objectMap [
            rml:reference "primaryProfession";
            rr:datatype xsd:string;
        ];
    ];
    rr:predicateObjectMap [
        rr:predicate ex:knownForTitles;
        rr:objectMap [
            rml:reference "knownForTitles";
            rr:datatype xsd:string;
        ];
    ].
  ```