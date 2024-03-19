from kg_core.utils.rdf import common_prefix_map
from rdflib import Graph
import re
from kg_core.utils.log import Logger


log = Logger("TurtleRepair")

class TurtleRepair():

    def __init__(self, data):
        self.data = data
        pass


    __prefix_name_pattern =re.compile("(^|\s+)([^<]\w*):")

    def __extract_used_prefix_names(self):
        lines = self.data.split('\n')
        prefix_names = []
        for line in lines:
            if not line.lower().lstrip().startswith('@prefix'):
                prefix_name_matches = self.__prefix_name_pattern.findall(line)
                for prefix_name_match in prefix_name_matches:
                    prefix_names.append(prefix_name_match[1])
        return set(prefix_names)

    def __extract_defined_prefix_names(self):
        lines = self.data.split('\n')
        prefix_names = []
        for line in lines:
            if line.lower().lstrip().startswith('@prefix'):
                prefix_name_matches = self.__prefix_name_pattern.findall(line)
                for prefix_name_match in prefix_name_matches:
                    prefix_names.append(prefix_name_match[1])
        return set(prefix_names)

    def repair_prefixes(self):
        if self.is_repaired():
            log.info("nothing to repair")
        else:
            prefix_names =  self.__extract_used_prefix_names() - self.__extract_defined_prefix_names()
            cpm = common_prefix_map()
            missing_prefix_definiton = ""
            for prefix_name in prefix_names:
                if prefix_name in cpm:
                    missing_prefix_definiton += f"@prefix {prefix_name}: <{cpm[prefix_name]}> .\n"
            self.data = missing_prefix_definiton + self.data
            log.info("prefixes repaired")

    def is_repaired(self) -> bool:
        try :
            Graph().parse(data=self.data, format='turtle')
            return True
        except Exception as e:
            return False
        
    def getData(self):
        return self.data

# test_data="""
#   @prefix : <http://mykg.org/resource/> .
# @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
# @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
# @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# <http://mykg.org/resource/1> a skos:Concept ;
#     skos:prefLabel "test" .

# dbo:Person a owl:Class .
# """

# def test():
#     tr = TurtleRepair(test_data)
#     print('repaired', tr.is_repaired())
#     tr.repair_prefixes()
#     print('repaired', tr.is_repaired())

# test()