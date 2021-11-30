from pyspark import SparkContext
from pyspark.sql import SparkSession


def start_spark() -> SparkSession:
    """
    Returns: (SparkSession) my Spark session
    """
    sc = SparkContext()
    sc.setLogLevel("ERROR")
    session = SparkSession(sparkContext=sc)
    print(f"\n{'#' * 100} \n SPARKY'FRUIT 360\n{'#' * 100}\n")
    return session
