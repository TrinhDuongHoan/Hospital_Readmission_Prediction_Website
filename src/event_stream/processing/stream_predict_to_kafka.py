from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, first, from_json
from pyspark.sql.types import IntegerType, StringType, StructField, StructType

from src.common.constants import (
    CATEGORICAL_FEATURES,
    DEFAULT_MODEL_PATH,
    KAFKA_INPUT_TOPIC,
    KAFKA_PREDICTION_TOPIC,
    NUMERIC_FEATURES,
    RISK_LABELS,
    SELECTED_FEATURES,
)
from src.common.logger import get_logger
from src.common.utils import risk_to_label
from src.event_stream.processing.transforms import apply_basic_stream_transforms
from src.event_stream.sinks.prediction_sink import build_prediction_message
from src.event_stream.sinks.sinks import create_kafka_sink_producer, publish_json_message
from src.features.online.feature_store import OnlineFeatureStore
from src.monitoring.service_metrics import ServiceMetrics, Timer


logger = get_logger("stream_predict_to_kafka")

feature_store = OnlineFeatureStore("artifacts/logs/online_feature_store.json")
metrics_tracker = ServiceMetrics("artifacts/logs/service_metrics.json")


def create_spark_session() -> SparkSession:
    spark = (
        SparkSession.builder
        .appName("HospitalStreamPredictionToKafka")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
        )
        .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


def get_bootstrap_servers() -> str:
    # host local: 127.0.0.1:9092
    # container/Airflow: kafka:29092
    import os
    return os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")


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
    bootstrap_servers = get_bootstrap_servers()

    raw_df = (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrap_servers)
        .option("subscribe", KAFKA_INPUT_TOPIC)
        .option("startingOffsets", "earliest")
        .load()
    )

    parsed_df = (
        raw_df
        .selectExpr("CAST(value AS STRING) as json_str")
        .select(from_json(col("json_str"), schema).alias("data"))
        .select("data.*")
    )

    parsed_df = apply_basic_stream_transforms(parsed_df)

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


def load_model(model_path: str = DEFAULT_MODEL_PATH):
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    return joblib.load(path)


def preprocess_for_inference(pdf: pd.DataFrame) -> pd.DataFrame:
    pdf = pdf.copy()

    for col_name in SELECTED_FEATURES:
        if col_name not in pdf.columns:
            pdf[col_name] = None

    for col_name in CATEGORICAL_FEATURES:
        pdf[col_name] = pdf[col_name].fillna("missing").astype(str)

    for col_name in NUMERIC_FEATURES:
        pdf[col_name] = pd.to_numeric(pdf[col_name], errors="coerce").fillna(0)

    return pdf[SELECTED_FEATURES]


def persist_online_feature_rows(pdf: pd.DataFrame) -> None:
    for _, row in pdf.iterrows():
        entity_id = str(row["encounter_id"])
        feature_store.put(entity_id, row.to_dict())


def predict_and_publish(batch_df: DataFrame, batch_id: int) -> None:
    logger.info("Processing prediction batch_id=%s", batch_id)
    print(f"\n========== Publishing predictions for batch {batch_id} ==========")

    if batch_df.rdd.isEmpty():
        logger.info("Empty batch. Skip.")
        print("Empty batch. Skip.")
        return

    pdf = batch_df.toPandas()

    # Lưu snapshot online features vào feature store mock
    persist_online_feature_rows(pdf)

    model = load_model()
    X = preprocess_for_inference(pdf)
    probs = model.predict_proba(X)[:, 1]

    result_df = pdf[["encounter_id", "patient_nbr"]].copy()
    result_df["readmission_probability"] = probs
    result_df["risk_level"] = result_df["readmission_probability"].apply(
        lambda p: risk_to_label(
            p,
            high_threshold=RISK_LABELS["high_threshold"],
            medium_threshold=RISK_LABELS["medium_threshold"],
        )
    )

    producer = create_kafka_sink_producer(bootstrap_servers=get_bootstrap_servers())

    try:
        for _, row in result_df.iterrows():
            with Timer() as timer:
                message = build_prediction_message(
                    encounter_id=row["encounter_id"],
                    patient_nbr=row["patient_nbr"] if pd.notna(row["patient_nbr"]) else None,
                    readmission_probability=row["readmission_probability"],
                    risk_level=row["risk_level"],
                )

                publish_json_message(
                    producer=producer,
                    topic=KAFKA_PREDICTION_TOPIC,
                    key=str(message["encounter_id"]),
                    payload=message,
                )

            metrics_tracker.record_prediction(
                risk_level=message["risk_level"],
                latency_ms=timer.elapsed_ms,
            )

            logger.info("Published prediction: %s", message)
            print(f"Published prediction: {message}")
    finally:
        producer.close()


def main():
    logger.info("Starting stream prediction to Kafka")
    spark = create_spark_session()
    feature_df = build_feature_stream(spark)

    query = (
        feature_df.writeStream
        .outputMode("complete")
        .foreachBatch(predict_and_publish)
        .start()
    )

    query.awaitTermination()


if __name__ == "__main__":
    main()