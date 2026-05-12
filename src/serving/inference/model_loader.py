from pathlib import Path
import joblib


MODEL_PATH = "artifacts/models/logistic_baseline.joblib"


def load_model(model_path: str = MODEL_PATH):
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = joblib.load(path)
    return model