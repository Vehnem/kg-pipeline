from typing import List
from SPARQLWrapper  import SPARQLWrapper, JSON
from kg_core.utils import sparql
from pyspark.sql import SparkSession
from pyspark import RDD


# Q6545185 - unique identifier
# TODO see wikidata.py

class IdExtractorSPARQL:
    def __init__(self):
        pass

    def get_external_ids_for_item(id: str) -> List[str]:
        pass

    def get_ids_for_external_id(external_id: str) -> List[str]:
        sparql_result = sparql.fetch_all_sparql_data(
        "https://query.wikidata.org/sparql", 1000, f"SELECT ?id WHERE {{ ?id <http://www.wikidata.org/prop/direct/P2147> '{external_id}' .}}")


class IdExtractorDBpeia:
    """
    Extracts list of entites with their wikidata id, and external id (, dbpedia id, wikipedia id)
    using the following DBpedia dumps
    - https://databus.dbpedia.org/dbpedia/wikidata/sameas-external/$LATEST/sameas-external.ttl.bzip2
    - TODO types

    """

    def __init__(self, config: dict):
        # Initialize SparkSession and SparkContext

        spark = SparkSession.builder.appName("IdExtractorDBpeia").getOrCreate()
        sc = spark.sparkContext

        # Load the text file into an RDD
        self.rdd = sc.textFile(config['sameas-external']).map(lambda line: line.split(' ',3))
        print(self.rdd.take(1))
        pass
    
    def extract_for_wikidata_id(self, id: str) -> List[str]:
        iri = "<http://wikidata.dbpedia.org/resource/" + id + '>'
        print(iri)

        taken = self.rdd.filter(lambda row: row[0] == iri).take(1)

        print(taken)
        pass
        

    def __get_node():
        pass


    def __get_namespace(iri: str) -> str:
        return iri.split('/')[2]
    

    def get_sameas_namespaces(self) -> List[str]:
        res: RDD = self.rdd.map(lambda row: IdExtractorDBpeia.__get_namespace(row[2]))
        
        print(res.distinct().collect())
        pass


    def extract_for_type(self, type: str) -> List[str]:
        pass