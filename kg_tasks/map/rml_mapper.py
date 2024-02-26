# from pyrml import x^
from rdflib import Graph
import subprocess, os
from kg_core.config import Config

# class PyRMLImpl:
#     """
#     This class is used to map the input file to RDF using the mapping file.
#     """
    
#     def __init__(self):
#         self.rml_converter = RMLConverter()

#     def apply_mapping(self, mapping_path, output_path):
#         """
#         maps the input file to RDF using the mapping file
#         """
#         # self.rml_converter.convert()
#         rdf_graph = self.rml_converter.convert(rml_mapping=mapping_path)
#         rdf_graph.serialize(destination=output_path, format='turtle')


class RMLMapperJavaImpl:
    """
    This class is used to map the input file to RDF using RML mapper Java
    """

    def __init__(self):
        binding = Config().bindings()['rml-mapper-java']
        self.entrypoint = binding['command'].split(' ')
        pass

    def apply_mapping(self, mapping_path):
        print(mapping_path)
        cmd = self.entrypoint + ['-m',mapping_path]
        stdout = subprocess.call(cmd)
        return stdout

