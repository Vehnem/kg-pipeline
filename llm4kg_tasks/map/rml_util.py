### Helps Moddifing RML Data ###
from rdflib import Graph

class RML_Wrapper:

    def __init__(self, rml_data):
        self.data = rml_data
        graph = Graph()
        graph.parse(data=rml_data, format="turtle")
        self.graph = graph

    def replace_data_source(self, source_path) -> str:
        pass

    def show(self):
        print(self.graph.serialize(format="turtle"))