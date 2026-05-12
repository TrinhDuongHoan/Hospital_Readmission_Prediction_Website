import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class AppConfig:
    app_name: str = "diabetes-mlops-streaming"
    environment: str = "dev"
    debug: bool = True


@dataclass
class KafkaConfig:
    bootstrap_servers: str = "127.0.0.1:9092"
    input_topic: str = "hospital-events"
    prediction_topic: str = "hospital-predictions"


@dataclass
class ModelConfig:
    model_path: str = "artifacts/models/logistic_baseline.joblib"
    high_threshold: float = 0.7
    medium_threshold: float = 0.4


@dataclass
class Settings:
    app: AppConfig
    kafka: KafkaConfig
    model: ModelConfig


def _read_yaml(file_path: str | Path) -> dict[str, Any]:
    path = Path(file_path)
    if not path.exists():
        return {}

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


def load_settings(
    app_config_path: str = "configs/app.yaml",
    kafka_config_path: str = "configs/kafka.yaml",
    model_config_path: str = "configs/model.yaml",
) -> Settings:
    app_yaml = _read_yaml(app_config_path)
    kafka_yaml = _read_yaml(kafka_config_path)
    model_yaml = _read_yaml(model_config_path)

    app = AppConfig(
        app_name=os.getenv("APP_NAME", app_yaml.get("app_name", "diabetes-mlops-streaming")),
        environment=os.getenv("APP_ENV", app_yaml.get("environment", "dev")),
        debug=str(os.getenv("APP_DEBUG", app_yaml.get("debug", True))).lower() == "true",
    )

    kafka = KafkaConfig(
        bootstrap_servers=os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS",
            kafka_yaml.get("bootstrap_servers", "127.0.0.1:9092")
        ),
        input_topic=os.getenv(
            "KAFKA_INPUT_TOPIC",
            kafka_yaml.get("input_topic", "hospital-events")
        ),
        prediction_topic=os.getenv(
            "KAFKA_PREDICTION_TOPIC",
            kafka_yaml.get("prediction_topic", "hospital-predictions")
        ),
    )

    model = ModelConfig(
        model_path=os.getenv(
            "MODEL_PATH",
            model_yaml.get("model_path", "artifacts/models/logistic_baseline.joblib")
        ),
        high_threshold=float(
            os.getenv("MODEL_HIGH_THRESHOLD", model_yaml.get("high_threshold", 0.7))
        ),
        medium_threshold=float(
            os.getenv("MODEL_MEDIUM_THRESHOLD", model_yaml.get("medium_threshold", 0.4))
        ),
    )

    return Settings(app=app, kafka=kafka, model=model)