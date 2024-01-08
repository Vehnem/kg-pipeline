from rdflib import Graph
from rdflib.plugins.sparql import prepareQuery

# Load the RDF graph
graph = Graph()
graph.parse("your_graph_file.rdf", format="xml")

# Define the SPARQL query
query = prepareQuery("""
    SELECT ?subject ?predicate ?object
    WHERE {
        ?subject ?predicate ?object .
    }
""")

# Execute the query and iterate over the results
results = graph.query(query)
for row in results:
    subject = row.subject
    predicate = row.predicate
    object = row.object
    print(f"Subject: {subject}, Predicate: {predicate}, Object: {object}")
