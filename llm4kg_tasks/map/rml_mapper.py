from pyrml import RMLConverter
import os

# Create an instance of the class RMLConverter.
rml_converter = RMLConverter()

'''
Invoke the method convert on the instance of class RMLConverter by:
 - using the file examples/artist/artist-map.ttl (see the examples in this repo);
 - obtaining an RDF graph as output.
'''
# rml_file_path = os.path.join('examples', 'artists', 'artist-map.ttl')
rdf_graph = rml_converter.convert(rml_mapping="/home/marvin/src/kg-pipeline/examples/rml2.ttl")

# Print the triples contained into the RDF graph.
for s,p,o in rdf_graph:
    print(s, p, o)