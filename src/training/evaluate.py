import json
from pathlib import Path
# import pandas as pd 
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

from src.training.preprocess import preprocess_pipeline

MODEL_PATH = "artifacts/models/logistic_baseline.joblib"
METRICS_PATH = "artifacts/metrics/logistic_baseline_metrics.json"

def evaluate_model():
    """Evaluate the trained logistic regression model on the test set and save the evaluation metrics."""

    X_train, X_test, y_train, y_test, categorical_features, numerical_features = preprocess_pipeline("data/raw/diabetic_data.csv")

    model = joblib.load(MODEL_PATH)

    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]


    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_proba),
        "average_precision": average_precision_score(y_test, y_proba)
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f)

    print("Metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    print("\nClassification report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    print(f"\nMetrics saved to: {METRICS_PATH}")

if __name__ == "__main__":
    evaluate_model()
