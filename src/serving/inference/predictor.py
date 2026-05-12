import pandas as pd

from src.serving.inference.model_loader import load_model
from src.serving.inference.postprocess import build_prediction_response


class ReadmissionPredictor:
    def __init__(self):
        self.model = load_model()

    def predict_one(self, payload: dict) -> dict:
        df = pd.DataFrame([payload])
        prob = self.model.predict_proba(df)[0, 1]
        return build_prediction_response(prob)