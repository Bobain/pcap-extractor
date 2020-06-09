from src.python.utils import dir_walk_apply
import os
import src.python.env as env
from pyspark.sql import SparkSession
from zat import log_to_sparkdf


# Spin up a local Spark Session
# os.environ["JAVA_HOME"] = env.JAVA_HOME
spark = (
    SparkSession.builder.master(env.SPARK_MASTER).appName("my_awesome").getOrCreate()
)


def is_zeek_file(file_path):
    root, f = os.path.split(file_path)
    return (
        ((root.split(os.path.sep)[-1] == ".zeek.logs") or f.endswith(".log"))
        and os.path.isfile(file_path)
        and not f.startswith(".")
    )


def apply_zeek(file_path, dir_path_out):
    spark_it = log_to_sparkdf.LogToSparkDF(spark)
    spark_df = spark_it.create_dataframe(file_path)
    spark_df.write.parquet(
        os.path.join(dir_path_out, os.path.split(file_path)[-1] + ".parquet"),
        compression="snappy",
    )


if __name__ == "__main__":
    dir_walk_apply(env.ROOT_DIR, env.TARGET_DIR, apply_zeek, condition_func=is_zeek_file)
