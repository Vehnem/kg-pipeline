"""Wikidata Sparql Helper object"""

from SPARQLWrapper import SPARQLWrapper


class WikidataSparqlHelper(object):
    """Wikidata Sparql Helper object"""

    __query="""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>

    SELECT DISTINCT ?property ?formaterUrl WHERE {
    ?propertyEntity wdt:P1630 ?formaterUrl .
    ?propertyEntity <http://wikiba.se/ontology#directClaim> ?property .
    wd:Q44578 ?property ?o .
    }
    """


    def __init__(self):
        pass


    def getProperties(self) -> list[str]:
        
        sq = SPARQLWrapper('https://query.wikidata.org/sparql')
        sq.setQuery(self.__query)
        sq.setReturnFormat('json')
        json = sq.query().convert()

        properties = []
        for binding in json['results']['bindings']:
            properties.append({'id':binding['property']['value'],'formaterUrl':binding['formaterUrl']['value']})
        return properties