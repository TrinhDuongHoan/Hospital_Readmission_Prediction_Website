from pathlib import Path

import pandas as pd

from src.common.constants import RAW_DATA_PATH, MISSING_VALUES
from src.common.logger import get_logger
from src.common.utils import ensure_dir
from src.features.mappings import (
    diagnosis_to_group,
    normalize_change,
    normalize_diabetes_med,
    normalize_gender,
    normalize_medical_specialty,
)


logger = get_logger("offline_features")


def load_raw_data(file_path: str = RAW_DATA_PATH) -> pd.DataFrame:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    df = pd.read_csv(
        path,
        na_values=MISSING_VALUES,
        low_memory=False,
        dtype={"diag_1": "str", "diag_2": "str", "diag_3": "str"},
    )
    return df


def build_offline_features(df: pd.DataFrame) -> pd.DataFrame:
    feat_df = df.copy()

    feat_df["medical_specialty"] = feat_df["medical_specialty"].apply(normalize_medical_specialty)
    feat_df["gender"] = feat_df["gender"].apply(normalize_gender)
    feat_df["change"] = feat_df["change"].apply(normalize_change)
    feat_df["diabetesMed"] = feat_df["diabetesMed"].apply(normalize_diabetes_med)

    feat_df["diag_1_group"] = feat_df["diag_1"].apply(diagnosis_to_group)
    feat_df["diag_2_group"] = feat_df["diag_2"].apply(diagnosis_to_group)
    feat_df["diag_3_group"] = feat_df["diag_3"].apply(diagnosis_to_group)

    feat_df["utilization_total"] = (
        feat_df["number_outpatient"].fillna(0)
        + feat_df["number_emergency"].fillna(0)
        + feat_df["number_inpatient"].fillna(0)
    )

    feat_df["lab_med_ratio"] = (
        feat_df["num_lab_procedures"].fillna(0)
        / feat_df["num_medications"].replace(0, pd.NA)
    ).fillna(0)

    feat_df["is_readmitted_30"] = (feat_df["readmitted"] == "<30").astype(int)

    return feat_df


def save_offline_features(df: pd.DataFrame, output_path: str = "data/gold/offline_features.csv") -> str:
    ensure_dir(Path(output_path).parent)
    df.to_csv(output_path, index=False)
    return output_path


def main():
    logger.info("Loading raw data...")
    df = load_raw_data()

    logger.info("Building offline features...")
    feat_df = build_offline_features(df)

    output_path = save_offline_features(feat_df)
    logger.info("Saved offline features to %s", output_path)
    logger.info("Output shape: %s", feat_df.shape)


if __name__ == "__main__":
    main()