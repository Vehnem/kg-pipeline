from kg_core.utils.sparql import fetch_all_sparql_data
from pyspark.sql import SparkSession

def test_sparql_all_data():
    sparql_results = fetch_all_sparql_data(
        "http://dbpedia.org/sparql", 
        1000, 
        """
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?sub WHERE {
        ?sub a dbo:VideoGame .
        }
        """)
    print(len(sparql_results))
    
# def test_draft():
#     spark = SparkSession.builder.appName("IdExtractorDBpeia").getOrCreate()
#     sc = spark.sparkContext

#     # Load the text file into an RDD
#     self.rdd = sc.textFile(config['sameas-external']).map(lambda line: line.split(' ',3))