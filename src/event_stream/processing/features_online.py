from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, first
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("HospitalOnlineFeatures")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1"
        )
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")
    return spark


def get_event_schema() -> StructType:
    return StructType([
        StructField("event_type", StringType(), True),
        StructField("event_time", StringType(), True),
        StructField("encounter_id", IntegerType(), True),
        StructField("patient_nbr", IntegerType(), True),

        StructField("race", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("age", StringType(), True),
        StructField("admission_type_id", IntegerType(), True),
        StructField("admission_source_id", IntegerType(), True),
        StructField("medical_specialty", StringType(), True),
        StructField("diag_1", StringType(), True),
        StructField("diag_2", StringType(), True),
        StructField("diag_3", StringType(), True),

        StructField("num_lab_procedures", IntegerType(), True),
        StructField("max_glu_serum", StringType(), True),
        StructField("A1Cresult", StringType(), True),
        StructField("number_diagnoses", IntegerType(), True),

        StructField("num_medications", IntegerType(), True),
        StructField("change", StringType(), True),
        StructField("diabetesMed", StringType(), True),

        StructField("discharge_disposition_id", IntegerType(), True),
        StructField("time_in_hospital", IntegerType(), True),
        StructField("num_procedures", IntegerType(), True),
        StructField("number_outpatient", IntegerType(), True),
        StructField("number_emergency", IntegerType(), True),
        StructField("number_inpatient", IntegerType(), True),
    ])


def build_feature_stream():
    spark = create_spark_session()
    schema = get_event_schema()

    raw_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "127.0.0.1:9092")
        .option("subscribe", "hospital-events")
        .option("startingOffsets", "earliest")
        .load()
    )

    parsed_df = (
        raw_df
        .selectExpr("CAST(value AS STRING) as json_str")
        .select(from_json(col("json_str"), schema).alias("data"))
        .select("data.*")
    )

    feature_df = (
        parsed_df
        .groupBy("encounter_id")
        .agg(
            first("patient_nbr", ignorenulls=True).alias("patient_nbr"),
            first("race", ignorenulls=True).alias("race"),
            first("gender", ignorenulls=True).alias("gender"),
            first("age", ignorenulls=True).alias("age"),
            first("admission_type_id", ignorenulls=True).alias("admission_type_id"),
            first("admission_source_id", ignorenulls=True).alias("admission_source_id"),
            first("medical_specialty", ignorenulls=True).alias("medical_specialty"),
            first("diag_1", ignorenulls=True).alias("diag_1"),
            first("diag_2", ignorenulls=True).alias("diag_2"),
            first("diag_3", ignorenulls=True).alias("diag_3"),
            first("num_lab_procedures", ignorenulls=True).alias("num_lab_procedures"),
            first("max_glu_serum", ignorenulls=True).alias("max_glu_serum"),
            first("A1Cresult", ignorenulls=True).alias("A1Cresult"),
            first("number_diagnoses", ignorenulls=True).alias("number_diagnoses"),
            first("num_medications", ignorenulls=True).alias("num_medications"),
            first("change", ignorenulls=True).alias("change"),
            first("diabetesMed", ignorenulls=True).alias("diabetesMed"),
            first("discharge_disposition_id", ignorenulls=True).alias("discharge_disposition_id"),
            first("time_in_hospital", ignorenulls=True).alias("time_in_hospital"),
            first("num_procedures", ignorenulls=True).alias("num_procedures"),
            first("number_outpatient", ignorenulls=True).alias("number_outpatient"),
            first("number_emergency", ignorenulls=True).alias("number_emergency"),
            first("number_inpatient", ignorenulls=True).alias("number_inpatient"),
        )
    )

    return feature_df


def main():
    feature_df = build_feature_stream()

    query = (
        feature_df.writeStream
        .format("console")
        .outputMode("complete")
        .option("truncate", False)
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()