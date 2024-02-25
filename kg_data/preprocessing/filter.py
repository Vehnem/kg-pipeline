from pyspark.sql import SparkSession
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode
import csv

class Filter(object):
    """Filter object"""

    def __init__(self):
        pass

    def join(self, pathToFile1, pathToFile2, column1, column2):
        """Filter the dataframe by the property and formaterUrl"""
        # Create a SparkSession
        spark = SparkSession.builder.getOrCreate()

        # Read the first CSV file
        df1 = spark.read.csv(pathToFile1, header=True, inferSchema=True)

        # Read the second CSV file
        df2 = spark.read.csv(pathToFile2, header=True, inferSchema=True)

        # Join the two dataframes based on the specified column
        joined_df = df1.join(df2, df1[column1] == df2[column2], "inner")

        # Return the joined dataframe
        return joined_df
    

    def normalize_csv_file(self, pathToFile):
        # Create a SparkSession
        spark = SparkSession.builder.getOrCreate()

        # Read the CSV file
        df = spark.read.csv(pathToFile, header=True, inferSchema=True, sep='\t')

        df.show()

        # Normalize multi-value columns into single columns
        normalized_df = df.selectExpr("*", "split(knownForTitles, ',') as normalized_column") \
            .selectExpr("*", "explode(normalized_column) as flattened_column")

        # Return the normalized dataframe
        return normalized_df


    def get_column_names(self, csv_file_path):
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            return header
    # Filter().join("data/examples/imdb/.csv", "data/formaterUrl.csv", "id").show()
        

    def predicate_filter(self, filter):
        pass

    
Filter().normalize_csv_file("/home/marvin/src/llm4kg/data/examples/imdb/Q44578/name.basics.tsv").show()