from llm4kg_dataset.acquisition.wikidata.ids import IdExtractorDBpeia

def test_spark_dbpedia_extractor():

    config = {
        'sameas-external': '/home/marvin/workspace/data/dbpedia/wikidata/sameas-external/2022.12.01/sameas-external.ttl.bz2'
    }

    extractor = IdExtractorDBpeia(config)

    extractor.extract_for_wikidata_id("Q44578")

    pass

