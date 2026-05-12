import pandas as pd

from src.monitoring.feedback_loop import evaluate_feedback


def test_evaluate_feedback():
    df = pd.DataFrame({
        "readmission_probability": [0.8, 0.2, 0.7, 0.1],
        "target": [1, 0, 1, 0],
    })

    metrics = evaluate_feedback(df)

    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics