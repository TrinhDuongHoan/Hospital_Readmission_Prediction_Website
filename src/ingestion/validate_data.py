from pathlib import Path
import pandas as pd


MISSING_VALUES = ["?", "None", "NULL", "null", "NA", "N/A", ""]

REQUIRED_COLUMNS = [
    "encounter_id",
    "patient_nbr",
    "race",
    "gender",
    "age",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
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
    "max_glu_serum",
    "A1Cresult",
    "change",
    "diabetesMed",
    "readmitted",
]


def load_dataset(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_csv(path, na_values=MISSING_VALUES)


def validate_columns(df: pd.DataFrame) -> None:
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")


def missing_ratio_report(df: pd.DataFrame) -> pd.DataFrame:
    report = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_ratio": df.isna().mean().values
    }).sort_values(by="missing_ratio", ascending=False)
    return report


def categorical_preview(df: pd.DataFrame, cols: list[str], top_n: int = 10) -> None:
    for col in cols:
        print(f"\n=== {col} ===")
        print(df[col].value_counts(dropna=False).head(top_n))


def basic_validation_report(df: pd.DataFrame) -> None:
    print("Dataset shape:", df.shape)

    print("\nData types:")
    print(df.dtypes)

    print("\nTarget distribution:")
    print(df["readmitted"].value_counts(dropna=False))

    print("\nTop missing columns:")
    print(missing_ratio_report(df).head(15))

    categorical_preview(
        df,
        cols=["race", "gender", "age", "weight", "payer_code", "medical_specialty", "max_glu_serum", "A1Cresult"]
    )


if __name__ == "__main__":
    df = load_dataset("data/raw/diabetic_data.csv")
    validate_columns(df)
    basic_validation_report(df)