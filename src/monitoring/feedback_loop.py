from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.common.logger import get_logger


logger = get_logger("monitoring.feedback_loop")


def merge_predictions_with_labels(
    prediction_path: str,
    ground_truth_path: str,
) -> pd.DataFrame:
    pred_path = Path(prediction_path)
    gt_path = Path(ground_truth_path)

    if not pred_path.exists():
        raise FileNotFoundError(f"Prediction file not found: {prediction_path}")
    if not gt_path.exists():
        raise FileNotFoundError(f"Ground truth file not found: {ground_truth_path}")

    pred_df = pd.read_csv(pred_path)
    gt_df = pd.read_csv(gt_path)

    merged = pred_df.merge(gt_df, on="encounter_id", how="inner")
    return merged


def evaluate_feedback(
    merged_df: pd.DataFrame,
    prob_col: str = "readmission_probability",
    label_col: str = "target",
    threshold: float = 0.5,
) -> dict:
    eval_df = merged_df.copy()
    eval_df["pred_label"] = (eval_df[prob_col] >= threshold).astype(int)

    y_true = eval_df[label_col].astype(int)
    y_pred = eval_df["pred_label"].astype(int)

    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "num_rows": int(len(eval_df)),
    }

    return metrics


def main():
    prediction_path = "artifacts/metrics/batch_predictions.csv"
    ground_truth_path = "artifacts/metrics/ground_truth_feedback.csv"

    merged_df = merge_predictions_with_labels(prediction_path, ground_truth_path)
    metrics = evaluate_feedback(merged_df)

    logger.info("Feedback evaluation metrics: %s", metrics)
    print(metrics)


if __name__ == "__main__":
    main()