from kg_core.metrics.ontology import HiearchyBasedScores
from rdflib import Graph
import json

ONTOLOGY_DATA="""
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix xsd: <http://www.w3.org/2001/XMLSchema#>.
@prefix owl: <http://www.w3.org/2002/07/owl#>.
@base <http://mykg.org/ontology/>.

<Agent> a owl:Class .

<Person> a owl:Class ;
    rdfs:subClassOf <Agent> .

<name> a owl:DatatypeProperty ;
    rdfs:domain <Person> ;
    rdfs:range rdfs:Literal .

<age> a owl:DatatypeProperty ;
    rdfs:domain <Person> ;
    rdfs:range xsd:integer .

<interactsWith> a owl:ObjectProperty ;
    rdfs:domain <Person> ;
    rdfs:range <Person> .

<Teacher> a owl:Class ;
   rdfs:subClassOf <Person> .

<teaches> a owl:ObjectProperty ;
    rdfs:domain <Teacher> ;
    rdfs:range <Person> ;
    rdfs:subPropertyOf <interactsWith> .
"""

TRIPLES_REF="""
@prefix : <http://mykg.org/ontology/>.
@base <http://mykg.org/>.

<Bob> a :Teacher ;
    :name "Bob" ;
    :age "25"^^<xsd:integer> ;
    :teaches <Alice> .

<Alice> a :Person ;
    :name "Alice" ;
    :age "30"^^<xsd:integer> .
"""

TRIPLES_TEST = """
@prefix : <http://mykg.org/ontology/>.
@base <http://mykg.org/resource/>.

<Bob> a :Person ;
    :name "Bob" ;
    :age "25"^^<xsd:integer> ;
    :interactsWith <Alice> .

<Alice> a :Person ;
    :name "Alice" ;
    :age "30"^^<xsd:integer> .
"""





def test_hbs():
    graph_onto = Graph().parse(data=ONTOLOGY_DATA, format="turtle")
    graph_ref = Graph().parse(data=TRIPLES_REF, format="turtle")
    graph_test = Graph().parse(data=TRIPLES_TEST, format="turtle")
    hbs = HiearchyBasedScores(graph_onto, graph_ref, graph_test)

    # class_sim_score = hbs.class_sim_score()
    # property_sim_score = hbs.property_sim_score()
    print("Class Scores Relaxed")
    print(json.dumps(hbs.class_sim_scores(), indent=2))
    print("Property Scores Relaxed")
    print(json.dumps(hbs.property_sim_scores(), indent=2))


def test_real():
    with open("kg_tests/resources/hiera_score_onto.ttl", "r") as f:
        onto = f.read()

    with open("kg_tests/resources/hiera_score_ref.ttl", "r") as f:
        ref = f.read()

    with open("kg_tests/resources/hiera_score_test.ttl", "r") as f:
        test = f.read()

    graph_onto = Graph().parse(data=onto, format="turtle")
    graph_ref = Graph().parse(data=ref, format="turtle")
    graph_test = Graph().parse(data=test, format="turtle")
    hbs = HiearchyBasedScores(graph_onto, graph_ref, graph_test)

    print("Class Scores Relaxed")
    # print(json.dumps(hbs.class_sim_scores(), indent=2))
    print("Property Scores Relaxed")
    dbo = "http://dbpedia.org/ontology/"

    propertyList = [dbo+"starring", dbo+"editor", dbo+"producer", dbo+"editing", dbo+"director", dbo+"composer", dbo+"runtime", dbo+"birthYear", dbo+"genre", dbo+"name", dbo+"title", dbo+"startYear"]
    somedict = hbs.checkProperties(propertyList)
    # del somedict['p_ref']
    # del somedict['p_test']
    # del somedict['s_alings']
    # del somedict['p_aligns']
    # del somedict['precision_scores']
    print(json.dumps(somedict, indent=2))