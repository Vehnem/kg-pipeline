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

## Example Snippets

## Indentified Sources

| name | namesace | domain | description |
| --- | --- | --- | --- |
| IMDB | https://www.imdb.com/ | CreativeWork | Contains information about actors,artists,movies,songs |
| DBpedia | | | 
| Wikipedia | | | 
| Wikidata | | |

### IMDB

```
name.basics.tsv.gz
nconst	primaryName	birthYear	deathYear	primaryProfession	knownForTitles
nm0000001	Fred Astaire	1899	1987	soundtrack,actor,miscellaneous	tt0053137,tt0072308,tt0031983,tt0050419

title.akas.tsv.gz
titleId	ordering	title	region	language	types	attributes	isOriginalTitle
tt0000001	1	Карменсіта	UA	\N	imdbDisplay	\N	0

title.basics.tsv.gz
tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres
tt0000001	short	Carmencita	Carmencita	0	1894	\N	1	Documentary,Short

title.crew.tsv.gz
tconst	directors	writers
tt0000001	nm0005690	\N

title.episode.tsv.gz
tconst	parentTconst	seasonNumber	episodeNumber
tt0041951	tt0041038	1	9

title.principals.tsv.gz
tconst	ordering	nconst	category	job	characters
tt0000001	1	nm1588970	self	\N	["Self"]

title.ratings.tsv.gz
tconst	averageRating	numVotes
tt0000001	5.7	2015
```
|   tconst|ordering|               title|region|language|      types|attributes|isOriginalTitle|titleType|        primaryTitle|       originalTitle|isAdult|startYear|endYear|runtimeMinutes|         genres|directors|  writers|parentTconst|seasonNumber|episodeNumber|ordering|   nconst|category|     job|characters|averageRating|numVotes|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|tt0001170|       1|A Cowboy's Vindic...|    US|      \N|imdbDisplay|        \N|              0|    short|A Cowboy's Vindic...|A Cowboy's Vindic...|      0|     1910|     \N|            \N|  Short,Western|nm0001908|nm0001908|        NULL|        NULL|         NULL|      10|nm0607104|   actor|      \N|        \N|         NULL|    NULL|