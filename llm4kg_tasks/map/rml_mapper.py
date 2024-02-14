# from pyrml import x^
from pyrml import RMLConverter
from rdflib import Graph
import os
import subprocess

class PyRMLImpl:
    """
    This class is used to map the input file to RDF using the mapping file.
    """
    
    def __init__(self):
        self.rml_converter = RMLConverter()
    

    def replace_source(self, mapping_path, source_path) -> str:
        g = Graph()
        g.parse(mapping_path)
        g.update(
            '''
            DELETE { ?s <http://semweb.mmlab.be/ns/rml#source> ?o . }
            INSERT { ?s <http://semweb.mmlab.be/ns/rml#source> "'''+source_path+'''" .}
            WHERE { ?s <http://semweb.mmlab.be/ns/rml#source> ?o . }
            '''
        )
        return g.serialize(format="turtle")


    def apply_mapping(self, mapping_path, output_path):
        """
        maps the input file to RDF using the mapping file
        """
        # self.rml_converter.convert()
        rdf_graph = self.rml_converter.convert(rml_mapping=mapping_path)
        rdf_graph.serialize(destination=output_path, format='turtle')


class RMLMapperJavaImpl:
    """
    This class is used to map the input file to RDF using RML mapper Java
    """

    def __init__(self):
        pass

    def apply_mapping(self, mapping_path, output_path):
        stdout = subprocess.call([
            '/home/marvin/.sdkman/candidates/java/current/bin/java', 
            '-jar', 
            '/home/marvin/workspace/code/rmlmapper-java/target/rmlmapper-6.5.1-r0-all.jar',
            '-m',
            mapping_path
            ])
        return stdout

