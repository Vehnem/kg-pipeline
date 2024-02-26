from pyspark import RDD
from pyspark.sql import DataFrame
from kg_data.connector.wiki.wikidata import IdExtractorDBpeia
from typing import List
from SPARQLWrapper  import SPARQLWrapper, JSON
from kg_core.utils import sparql
from pyspark.sql import SparkSession

# def test_spark_dbpedia_extractor():

#     config = {
#         'sameas-external': '/home/marvin/workspace/data/dbpedia/wikidata/sameas-all-wikis/2022.12.01/sameas-all-wikis.ttl.bz2'
#     }

#     extractor = IdExtractorDBpeia(config)

#     # extractor.extract_for_wikidata_id("Q44578")

#     extractor.get_sameas_namespaces()

#     pass

def __extract_nodes_from_ntriple_line(line: str)-> List[str]:
    split = line.split(' ', 4)
    s_part: str = split[0]
    s = s_part[1:-1]
    p_part: str = split[1]
    p = p_part[1:-1]
    o_part: str = split[2]
    o = o_part[1:-1]
    return [s,p,o]


def test_more():
    
    config = {
    }

    # file = '/home/marvin/workspace/data/dbpedia/wikidata/mappingbased-objects-uncleaned/2022.12.01/mappingbased-objects-uncleaned.ttl.bz2'

    spark = SparkSession.builder.appName("workbench").getOrCreate()
    sc = spark.sparkContext

    # rdd: RDD = sc.textFile(file)
    # rdf_rdd: RDD = rdd.map(__extract_nodes_from_ntriple_line)

    # # print(rdf_rdd.take(3))
    # filtered_rdf_rdd: RDD = rdf_rdd.filter(lambda triple: triple[1] == "http://www.w3.org/2000/01/rdf-schema#seeAlso")
    # rdf_df: DataFrame = filtered_rdf_rdd.toDF(['s','p','o'])
    
    # rdf_df.write.parquet('test.parquet')

    # rdf_df: DataFrame = spark.read.parquet('test.parquet')

    # filtered_rdf_df: DataFrame = rdf_df.filter(rdf_df.o.startswith('http://www.imdb.com/'))

    # print(filtered_rdf_df.count())
    # RESULT 782797 links between Wikidata and IMDB

    # filtered_rdf_df.select('s','o').write.parquet("wkd_imdb_links.parquet")

    # all_wikis_rdd: RDD = sc.textFile('/home/marvin/workspace/data/dbpedia/wikidata/sameas-all-wikis/2022.12.01/sameas-all-wikis.ttl.bz2').map(__extract_nodes_from_ntriple_line)
    # all_wikis_df: DataFrame = all_wikis_rdd.toDF(['wikidata','p','dbpedia'])
    # filterd_all_wikis_df: DataFrame = all_wikis_df.filter(all_wikis_df.dbpedia.startswith('http://dbpedia.org/resource')).select('wikidata','dbpedia')
    # # filterd_all_wikis_df.select('s','o').show()
    
    # wkd_imdb_df: DataFrame = spark.read.parquet("wkd_imdb_links.parquet")

    # # wkd_imdb_df.
    # joined_df = wkd_imdb_df.join(filterd_all_wikis_df,  wkd_imdb_df.s  == filterd_all_wikis_df.wikidata , 'inner')

    # joined_df.write.parquet('wkd_imdb_dbpedia_links.parquet')

    # df: DataFrame = spark.read.parquet('wkd_imdb_dbpedia_links.parquet')
    # joined = df.withColumnRenamed('o','imdb').select('wikidata','dbpedia','imdb')

    # joined.coalesce(1).write.csv('links_wkd_imdb_dbpedia.csv', header=True)

    #### Process Links further ####
    
    pass