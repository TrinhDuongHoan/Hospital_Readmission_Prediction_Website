from pathlib import Path

import joblib
import pandas as pd
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, from_json, first
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


MODEL_PATH = "artifacts/models/logistic_baseline.joblib"

MODEL_FEATURES = [
    "race",
    "gender",
    "age",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
    "medical_specialty",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "diag_1",
    "diag_2",
    "diag_3",
    "number_diagnoses",
    "change",
    "diabetesMed",
]


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("HospitalStreamPrediction")
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


def build_feature_stream(spark: SparkSession) -> DataFrame:
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
            first("discharge_disposition_id", ignorenulls=True).alias("discharge_disposition_id"),
            first("admission_source_id", ignorenulls=True).alias("admission_source_id"),
            first("time_in_hospital", ignorenulls=True).alias("time_in_hospital"),
            first("medical_specialty", ignorenulls=True).alias("medical_specialty"),
            first("num_lab_procedures", ignorenulls=True).alias("num_lab_procedures"),
            first("num_procedures", ignorenulls=True).alias("num_procedures"),
            first("num_medications", ignorenulls=True).alias("num_medications"),
            first("number_outpatient", ignorenulls=True).alias("number_outpatient"),
            first("number_emergency", ignorenulls=True).alias("number_emergency"),
            first("number_inpatient", ignorenulls=True).alias("number_inpatient"),
            first("diag_1", ignorenulls=True).alias("diag_1"),
            first("diag_2", ignorenulls=True).alias("diag_2"),
            first("diag_3", ignorenulls=True).alias("diag_3"),
            first("number_diagnoses", ignorenulls=True).alias("number_diagnoses"),
            first("change", ignorenulls=True).alias("change"),
            first("diabetesMed", ignorenulls=True).alias("diabetesMed"),
        )
    )

    return feature_df


def risk_to_label(prob: float) -> str:
    if prob >= 0.7:
        return "high"
    if prob >= 0.4:
        return "medium"
    return "low"


def load_model():
    path = Path(MODEL_PATH)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    return joblib.load(path)


def preprocess_for_inference(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.copy()

    for col_name in MODEL_FEATURES:
        if col_name not in pdf.columns:
            pdf[col_name] = None

    # fill missing giống logic inference đơn giản
    categorical_cols = [
        "race", "gender", "age", "medical_specialty",
        "diag_1", "diag_2", "diag_3", "change", "diabetesMed"
    ]
    numeric_cols = [
        "admission_type_id", "discharge_disposition_id", "admission_source_id",
        "time_in_hospital", "num_lab_procedures", "num_procedures",
        "num_medications", "number_outpatient", "number_emergency",
        "number_inpatient", "number_diagnoses"
    ]

    for c in categorical_cols:
        pdf[c] = pdf[c].fillna("missing").astype(str)

    for c in numeric_cols:
        pdf[c] = pd.to_numeric(pdf[c], errors="coerce").fillna(0)

    return pdf[MODEL_FEATURES]


def predict_batch(batch_df: DataFrame, batch_id: int) -> None:
    print(f"\n========== Predicting batch {batch_id} ==========")

    if batch_df.rdd.isEmpty():
        print("Empty batch. Skip.")
        return

    pdf = batch_df.toPandas()

    model = load_model()
    X = preprocess_for_inference(pdf)
    probs = model.predict_proba(X)[:, 1]

    result_df = pdf[["encounter_id", "patient_nbr"]].copy()
    result_df["readmission_probability"] = probs
    result_df["risk_level"] = result_df["readmission_probability"].apply(risk_to_label)

    print(result_df.to_string(index=False))


def main():
    spark = create_spark_session()
    feature_df = build_feature_stream(spark)

    query = (
        feature_df.writeStream
        .outputMode("complete")
        .foreachBatch(predict_batch)
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()