from pyspark.sql import SparkSession
from pyspark.sql.functions import col

class SparkPreprocess:
    def __init__(self):
        # self.csv_path = csv_path
        # self.column_names = column_names
        # self.df = self.spark.read.option("delimiter", " ").csv(self.csv_path)
        # self.filter_column = filter_column
        # self.filter_value = filter_value
        self.spark = SparkSession.builder.getOrCreate()


    @staticmethod
    def unwrappNT(row):
        arr = row.split(" ")
        if(len(arr) < 3):
            raise ValueError("Invalid line: " + row)
        else:
            s = arr[0].replace("<", "").replace(">", "")
            p = arr[1].replace("<", "").replace(">", "")
            o = arr[2].replace("<", "").replace(">", "")
            return (s, p, o)
    

    def join(self, df1, df2, join_column1, join_column2=None, join="inner"):
        if join_column2 is None:
            joined_df = df1.join(df2, join_column1, join)
        else:
            joined_df = df1.join(df2, df1[join_column1] == df2[join_column2],join)
        return joined_df


    def read_nt(self, nt_path):
        rdd = self.spark.sparkContext.textFile(nt_path)
        df = rdd.map(lambda row: SparkPreprocess.unwrappNT(row)).toDF(["s", "p", "o"])
        return df


    def read_csv(self, csv_path, delimiter):
        df = self.spark.read.option("delimiter", delimiter).option("header",True).csv(csv_path)
        return df


    def rename_columns(self, df, column_names):
        renamed_df = df.toDF(*column_names)
        return renamed_df

    # def filter_values(self, df):
    #     filtered_df = df.filter(col(self.filter_column) == self.filter_value)
    #     return filtered_df




