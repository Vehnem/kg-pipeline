from kg_core.metrics.metrics import RDF_Similarity_Metrics
from rdflib import Graph

GRAPH_ONTOLOGY_DATA="""

"""
GRAPH_ONTOLOGY=Graph()
GRAPH_ONTOLOGY.parse(data=GRAPH_ONTOLOGY_DATA, format='turtle')

GRAPH_0_DATA="""
@base <http://mykg.org/>

<Alcie> a <Person> .

<Bob> a <Person> .
<Bob> <knows <Person/Alcie>> .

<Alice> a <Person> .
<Alice> <knows <Person/Bob>> .

"""
GRAPH_0=Graph()
GRAPH_0.parse(data=GRAPH_0_DATA, format='turtle')

GRAPH_A_DATA="""


"""

GRAPH_A=Graph()
GRAPH_A.parse(data=GRAPH_A_DATA, format='turtle')

def test_subejcts_fuzzy():

    metrics = RDF_Similarity_Metrics(GRAPH_0, GRAPH_A)
    print(metrics.subjects_classes_fuzzy())

