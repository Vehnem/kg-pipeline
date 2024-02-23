from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()
sc = spark.sparkContext


def generate_big_table_csvs(csvs: list[str]):
    for csv in csvs:
        print(csv)
    pass


def normalize_table():
    pass


def join_ids():
    pass