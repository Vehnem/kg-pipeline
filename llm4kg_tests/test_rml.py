### Test RML Mapper ###
from llm4kg_tasks.map.rml_mapper import RMLMapperJavaImpl

def test_rml_mapper():
    mapper = RMLMapperJavaImpl()
    mapper.apply_mapping(
        mapping_path='./llm4kg_tests/examples/rml/test.csv.rml.ttl',
        output_path='test_rml_output.ttl', 
    )

# def test_replace():
#     mapper = RMLMapper()
#     mapper.replace_source('./llm4kg_tests/examples/rml/test.rml.ttl',"someSource")
#     pass