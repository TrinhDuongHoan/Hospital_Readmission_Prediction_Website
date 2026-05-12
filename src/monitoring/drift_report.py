import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.common.constants import CATEGORICAL_FEATURES, NUMERIC_FEATURES
from src.common.logger import get_logger


logger = get_logger("monitoring.drift_report")


def numeric_drift(train_df: pd.DataFrame, online_df: pd.DataFrame) -> dict[str, Any]:
    report = {}

    for col in NUMERIC_FEATURES:
        if col not in train_df.columns or col not in online_df.columns:
            continue

        train_mean = pd.to_numeric(train_df[col], errors="coerce").mean()
        online_mean = pd.to_numeric(online_df[col], errors="coerce").mean()

        report[col] = {
            "train_mean": None if pd.isna(train_mean) else round(float(train_mean), 4),
            "online_mean": None if pd.isna(online_mean) else round(float(online_mean), 4),
            "abs_diff": None
            if pd.isna(train_mean) or pd.isna(online_mean)
            else round(abs(float(train_mean) - float(online_mean)), 4),
        }

    return report


def categorical_drift(train_df: pd.DataFrame, online_df: pd.DataFrame) -> dict[str, Any]:
    report = {}

    for col in CATEGORICAL_FEATURES:
        if col not in train_df.columns or col not in online_df.columns:
            continue

        train_mode = train_df[col].astype(str).mode()
        online_mode = online_df[col].astype(str).mode()

        report[col] = {
            "train_top": None if train_mode.empty else str(train_mode.iloc[0]),
            "online_top": None if online_mode.empty else str(online_mode.iloc[0]),
            "changed": (
                None
                if train_mode.empty or online_mode.empty
                else str(train_mode.iloc[0]) != str(online_mode.iloc[0])
            ),
        }

    return report


def generate_drift_report(
    train_df: pd.DataFrame,
    online_df: pd.DataFrame,
    output_path: str = "artifacts/logs/drift_report.json",
) -> dict[str, Any]:
    report = {
        "numeric_drift": numeric_drift(train_df, online_df),
        "categorical_drift": categorical_drift(train_df, online_df),
        "train_rows": int(len(train_df)),
        "online_rows": int(len(online_df)),
    }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info("Saved drift report to %s", output_path)
    return report


def main():
    train_path = "data/gold/offline_features.csv"
    online_path = "artifacts/logs/latest_online_features.csv"

    if not Path(train_path).exists():
        raise FileNotFoundError(f"Train feature file not found: {train_path}")
    if not Path(online_path).exists():
        raise FileNotFoundError(f"Online feature snapshot file not found: {online_path}")

    train_df = pd.read_csv(train_path)
    online_df = pd.read_csv(online_path)

    report = generate_drift_report(train_df, online_df)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()