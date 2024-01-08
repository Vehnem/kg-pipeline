# LLM4KG Dataset

This module contains the dataset generator.

The idea is to use external identifiers from one to another namespace to aquire new test data for integration

**Sub module description**


- **shade** - the shade module contains functions to shade entries of datasets to make them indecipherable of their origin |
- **examples** - contains small example data for testing
- **preprocessing**
- **acquisition**

## weak same As

## Wikidata indentifiers

There is a vast amount of external indetifiers in wikidata

The idea is to use the external resources to generate benchmark data for knowledge graph construction



**Benefits**
- manually currated

**Limitations**
- some of these indentifiers might refer to related information but not information about the same (equivalent) thing
- Altough the entries in wikidata are often currated manually, for the external identifiers it is possible that a referenced resource is not representing the same thing as in wikidata.
For example a movie entry in wikidata can reference with an external identifier to an actor instead of an entry on an other site than wikidata.


## Wikidata intelanguage links

Wikidata interlanguage links are links between wikimedia projects.

https://wikipedia.org/wiki/Berlin links to https://de.wikipedia.org/wiki/Berlin or https://wikidata.org/item/Q64

## DBpedia External Links

## Indentified Sources

| name | namesace | domain | description |
| --- | --- | --- | --- |
| IMDB | https://www.imdb.com/ | CreativeWork | Contains information about actors,artists,movies,songs |
| DBpedia | | | 
| Wikipedia | | | 
| Wikidata | | |
