from SPARQLWrapper import SPARQLWrapper

sq = SPARQLWrapper('https://dbpedia.org/sparql')

types2 = ['TelevisionShow']
types = ['Person', 'Film', 'VideoGame', 'Band']

for type in types:
    for type2 in types2:
        if type == type2:
            continue

        sq.setQuery("SELECT (COUNT(?p) as ?cp) ?p { ?s a <http://dbpedia.org/ontology/"+type+"> . ?s ?p ?o . ?o a <http://dbpedia.org/ontology/"+type2+"> . } ORDER BY DESC(?cp)")
        sq.setReturnFormat('json')
        json = sq.query().convert()

        print("Relations between "+type+" and "+type2+":")

        for binding in json['results']['bindings']:
            print(type+','+type2+','+binding['cp']['value']+","+binding['p']['value'])
        print()