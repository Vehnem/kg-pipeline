### Helps Moddifing RML Data ###
from rdflib import Graph

class RML_Wrapper:

    def __init__(self, rml_graph: Graph):
        self.graph : Graph = rml_graph

    def replace_rml_source(self, source_path) -> str:
        self.graph.update(
            '''
            DELETE { ?s <http://semweb.mmlab.be/ns/rml#source> ?o . }
            INSERT { ?s <http://semweb.mmlab.be/ns/rml#source> "'''+source_path+'''" .}
            WHERE { ?s <http://semweb.mmlab.be/ns/rml#source> ?o . }
            '''
        )


    def show(self):
        print(self.graph.serialize(format="turtle"))