### 
from pyspark.sql import SparkSession, DataFrame, Row
from pyspark import RDD
from pyspark.sql.functions import explode
from pyspark.sql.types import StructType, StructField, ArrayType, StringType, IntegerType
from typing import Tuple, Iterable

fileNames = [
    "name.basics.tsv.bz2",
    # "title.akas.tsv.bz2",
    "title.basics.tsv.bz2",
    "title.crew.tsv.bz2",
    "title.episode.tsv.bz2",
    "title.principals.tsv.bz2",
    # "title.ratings.tsv.bz2",
]


def titleBasicsToDict(row: Row) -> dict:
    genres = list(str(row['genres']).split(','))
    resultDict = {
        'titleType' : row['titleType'],
        'primaryTitle' : row['primaryTitle'],
        'originalTitle' : row['originalTitle'],
        'isAdult' : row['isAdult'],
        'startYear' : row['startYear'],
        'endYear' : row['endYear'],
        'runtimeMinutes' : row['runtimeMinutes'],
        'genres' : genres
    }
    print(genres)
    return resultDict

def principalsToDict(row: Row) -> dict:
    return {
    #    'nconst' : row['nconst'],
        'ordering': row['ordering'],
        'category' : row['category'],
        'job' : row['job'],
        'characters' : row['characters']
    }


def nameBasicsToDict(row: Row) -> dict:
    return {
        # 'nconst' : row['nconst'],
        'primaryName' : row['primaryName'],
        'birthYear' : row['birthYear'],
        'deathYear' : row['deathYear'],
        # 'primaryProfession' : str(row['primaryProfession']).split(','),
        # 'knownForTitles' : str(row['knownForTitles']).split(',')
    }


def toFinalDict(row: Row) -> dict: 

    entry = {}

    entry.update({'id': row['tconst']})

    entry.update(row['titleBasics'])

    involvedPersons = []

    for person in row['principals_names']:
        involvedPerson = {}

        involvedPerson.update(person['nameBasics'])

        principlas_relation = person['principals']
        
        involvedPerson.update({
            'id': person['nconst'],
            'ordering': int(principlas_relation['ordering']),
            'category': principlas_relation['category']
            })

        involvedPersons.append(involvedPerson)

    involvedPersons.sort(key=lambda x: x['ordering'])

    entry.update({'involvedPeople': involvedPersons})

    return entry


class Imdb2JsonConverter:

    def __init__(self, config: dict):
        self.cofig = config
        pass

    
    def unwrap(self):
        pass


    def join(self):
        pass


    def convert(self):
        spark = SparkSession.builder.config("spark.driver.memory", "30g").getOrCreate()
        sc = spark.sparkContext

        dir=self.cofig['dir']


        ### First Grouping

        # titlePrincipals: DataFrame = spark.read.csv(dir+'title.principals.tsv.bz2', header=True, sep='\t').rdd.map(lambda row: Row(tconst = row['tconst'], nconst = row['nconst'], principals = principalsToDict(row))).toDF()

        # nameBasics: DataFrame = spark.read.csv(dir+'name.basics.tsv.bz2', header=True, sep='\t').rdd.map(lambda row: Row(nconstPerson = row['nconst'], nameBasics = nameBasicsToDict(row))).toDF()

        # joined_nameBasics_titlePrincipals: DataFrame = titlePrincipals.join(nameBasics, titlePrincipals.nconst == nameBasics.nconstPerson)

        # joined_nameBasics_titlePrincipals.write.parquet(dir+'joined_nameBasics_titlePrincipals.parquet', mode='overwrite')
    

        ### Second Grouping

        df: DataFrame  = spark.read.parquet(dir+'joined_nameBasics_titlePrincipals.parquet')

        # df.select('nameBasics').show(truncate=False)

        rdd: RDD = df.rdd 

        groupedRDD: RDD[Tuple[str,Iterable]] = rdd.groupBy(lambda row: row['tconst']).map(lambda tuple: Row(tconst= tuple[0], principals_names = list(tuple[1]))).toDF()

        # groupedSchema = StructField

        titleBasics: DataFrame = spark.read.csv(dir+'title.basics.tsv.bz2', header=True, sep='\t').limit(10).rdd.map(lambda row: Row(tconstBasics = row['tconst'], titleBasics = titleBasicsToDict(row)))

        titleBasicsSchema = StructType([
            StructField("tconstBasics", StringType(), True),
            StructField("titleBasics", StructType([
                StructField('titleType', StringType(), True),
                StructField('primaryTitle', StringType(), True),
                StructField('originalTitle', StringType(), True),
                StructField('isAdult', StringType(), True),
                StructField('startYear', StringType(), True),
                StructField('endYear', StringType(), True),
                StructField('runtimeMinutes', StringType(), True),
                StructField('genres', ArrayType(StringType()), True)
                ]))
            ])

        titleBasicsDf = spark.createDataFrame(titleBasics, titleBasicsSchema)

        joined_titelBasics_principals_nameBasics: DataFrame = groupedRDD.join(titleBasicsDf, groupedRDD.tconst == titleBasicsDf.tconstBasics)
        
        joined_titelBasics_principals_nameBasics.write.parquet(dir+'joined_titelBasics_principals_nameBasics.parquet', mode='overwrite')
        
        
        ### JSON Cleanup

        # finalRDD: RDD = spark.read.parquet(dir+'joined_titelBasics_principals_nameBasics.parquet').limit(10).rdd

        # finalDF: DataFrame = finalRDD.map(lambda row: toFinalDict(row)).toDF()

        # finalDF.printSchema()

        # finalDF.select('id',explode('genres')).show()

        # finalDF.write.option("multiLine", True).option("mode", "PERMISSIVE").json(dir+'finalDF.json', mode='overwrite')




        # titleCrew = spark.read.csv(dir+'title.crew.tsv.bz2', header=True, sep='\t')

        # titlePrincipals = spark.read.csv(dir+'title.principals.tsv.bz2', header=True, sep='\t').withColumnRenamed('tconst', 'tconstPrincipals').withColumnRenamed('nconst', 'nconstPrincipals')

        # titleBasics.join(titlePrincipals, titleBasics.tconstBasics == titlePrincipals.tconstPrincipals).show()

        # spark.read.csv(dir+'/name.*.tsv.bz2', header=True, sep='\t').show()

        pass