from __future__ import annotations

from pyspark.sql import DataFrame
from pyspark.sql.functions import col, lit, trim, when


def normalize_stream_fields(df: DataFrame) -> DataFrame:
    """
    Normalize selected string columns in the streaming DataFrame.
    """
    string_cols = [
        "race",
        "gender",
        "age",
        "medical_specialty",
        "diag_1",
        "diag_2",
        "diag_3",
        "max_glu_serum",
        "A1Cresult",
        "change",
        "diabetesMed",
    ]

    out = df
    for c in string_cols:
        if c in out.columns:
            out = out.withColumn(
                c,
                when(col(c).isNull(), lit("missing"))
                .otherwise(trim(col(c)))
            )

    return out


def add_stream_feature_flags(df: DataFrame) -> DataFrame:
    """
    Add a few derived flags to help online feature engineering.
    """
    out = df

    if "num_lab_procedures" in out.columns:
        out = out.withColumn(
            "has_many_labs",
            when(col("num_lab_procedures") >= 40, lit(1)).otherwise(lit(0))
        )

    if "number_inpatient" in out.columns:
        out = out.withColumn(
            "has_prior_inpatient_history",
            when(col("number_inpatient") > 0, lit(1)).otherwise(lit(0))
        )

    if "time_in_hospital" in out.columns:
        out = out.withColumn(
            "long_stay",
            when(col("time_in_hospital") >= 7, lit(1)).otherwise(lit(0))
        )

    return out


def apply_basic_stream_transforms(df: DataFrame) -> DataFrame:
    df = normalize_stream_fields(df)
    df = add_stream_feature_flags(df)
    return df