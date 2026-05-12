from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd


def ensure_dir(path: str | Path) -> Path:
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def timestamp_now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def safe_value(value: Any, default: Any = "missing") -> Any:
    if pd.isna(value):
        return default
    return value


def safe_int(value: Any, default: int = 0) -> int:
    try:
        if pd.isna(value):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if pd.isna(value):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_category(value: Any, default: str = "missing") -> str:
    if pd.isna(value):
        return default
    return str(value).strip()


def risk_to_label(prob: float, high_threshold: float = 0.7, medium_threshold: float = 0.4) -> str:
    if prob >= high_threshold:
        return "high"
    if prob >= medium_threshold:
        return "medium"
    return "low"