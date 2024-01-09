
from llm4kg_dataset.preprocessing.preprocess import SparkPreprocess

nt1 = "/home/marvin/src/kg-pipeline/target/raw_downloads/dbpedia/labels_lang=en.ttl.bz2"

csv0 = "/home/marvin/src/kg-pipeline/target/raw_downloads/imdb/datasets.imdbws.com/title.akas.tsv.gz"
csv1 = "/home/marvin/src/kg-pipeline/target/raw_downloads/imdb/datasets.imdbws.com/title.basics.tsv.gz"
csv2 = "/home/marvin/src/kg-pipeline/target/raw_downloads/imdb/datasets.imdbws.com/title.crew.tsv.gz"
csv3 = "/home/marvin/src/kg-pipeline/target/raw_downloads/imdb/datasets.imdbws.com/title.episode.tsv.gz"
csv4 = "/home/marvin/src/kg-pipeline/target/raw_downloads/imdb/datasets.imdbws.com/title.principals.tsv.gz"
csv5 = "/home/marvin/src/kg-pipeline/target/raw_downloads/imdb/datasets.imdbws.com/title.ratings.tsv.gz"

def test_spark_preprocess():
    sp = SparkPreprocess()
    df = sp.read_nt(nt1)
    df.show(10)


def test_spark_preprocess_join():
    sp = SparkPreprocess()
    df1 = sp.read_nt(nt1)
    df2 = sp.read_nt(nt1)
    joined_df = sp.join(df1, df2, "s","o","fullouter")
    joined_df.show(10)


def test_imdb_expand():
    sp = SparkPreprocess()
    df0 = sp.read_csv(csv0, "\t")
    df1 = sp.read_csv(csv1, "\t")
    df2 = sp.read_csv(csv2, "\t")
    df3 = sp.read_csv(csv3, "\t")
    df4 = sp.read_csv(csv4, "\t")
    df5 = sp.read_csv(csv5, "\t")

    df01 = sp.join(df0, df1, "titleId", "tconst", "outer").drop("titleId")
    df012 = sp.join(df01, df2, "tconst",  join="outer")
    df0123 = sp.join(df012, df3, "tconst", join="outer")
    df01234 = sp.join(df0123, df4, "tconst", join="outer")
    df012345 = sp.join(df01234, df5, "tconst", join="outer")

    df012345.write.csv("/home/marvin/src/kg-pipeline/target/imdb_titles_joined.csv", header=True, mode="overwrite")