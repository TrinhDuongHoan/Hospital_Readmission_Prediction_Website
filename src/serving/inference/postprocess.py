from src.common.constants import RISK_LABELS
from src.common.utils import risk_to_label


def build_prediction_response(prob: float) -> dict:
    return {
        "readmission_probability": round(float(prob), 4),
        "risk_level": risk_to_label(
            prob,
            high_threshold=RISK_LABELS["high_threshold"],
            medium_threshold=RISK_LABELS["medium_threshold"],
        ),
    }