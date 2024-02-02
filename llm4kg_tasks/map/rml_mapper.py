from pyrml import RMLConverter
import os

class RMLMapper:
    """
    This class is used to map the input file to RDF using the mapping file.
    """
    
    def __init__(self):
        self.rml_converter = RMLConverter()
        pass
    # Create an instance of the class RMLConverter.
    

    def apply_mapping(self, mapping_path, input_path, output_path):
        """
        maps the input file to RDF using the mapping file
        """
        rdf_graph = self.rml_converter.convert(rml_mapping=mapping_path)
        rdf_graph.serialize(destination=output_path, format='turtle')
        return rdf_graph


'''
Invoke the method convert on the instance of class RMLConverter by:
- using the file examples/artist/artist-map.ttl (see the examples in this repo);
- obtaining an RDF graph as output.
'''