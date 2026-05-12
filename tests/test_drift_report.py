import pandas as pd

from src.monitoring.drift_report import generate_drift_report


def test_generate_drift_report(tmp_path):
    train_df = pd.DataFrame({
        "num_lab_procedures": [10, 20],
        "race": ["Caucasian", "Caucasian"],
    })
    online_df = pd.DataFrame({
        "num_lab_procedures": [15, 30],
        "race": ["AfricanAmerican", "AfricanAmerican"],
    })

    output_path = tmp_path / "drift_report.json"
    report = generate_drift_report(train_df, online_df, str(output_path))

    assert "numeric_drift" in report
    assert "categorical_drift" in report