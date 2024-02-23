###Down Sampling of Datasets###
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import explode

class JsonSampler():
    
    def __init__(self, path):
        self.spark = SparkSession.builder.config("spark.driver.memory", "30g").getOrCreate()
        self.path = path
        pass
    
    
    def complete_sample_from(self, config: dict):
        """A complete sample contains all the"""
        # df = self.spark.read.json(self.path)
        # df.write.parquet(self.path+'.parquet', mode='overwrite')

        df = self.spark.read.parquet(self.path+'.parquet')
        df.createOrReplaceTempView("df")

        df.show()

        df.select('involvedPeople.birthYear').show()

        # self.spark.sql(f"SELECT DISTINCT explode(genres) FROM df LIMIT").show()