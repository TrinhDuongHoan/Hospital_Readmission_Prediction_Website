from typing import Any

from src.common.constants import KAFKA_PREDICTION_TOPIC
from src.common.logger import get_logger
from src.event_stream.sinks.sinks import create_kafka_sink_producer, publish_json_message


logger = get_logger(
    "stream.prediction_sink",
    log_file="artifacts/logs/prediction_sink.log",
)


def build_prediction_message(
    encounter_id: int,
    patient_nbr: int | None,
    readmission_probability: float,
    risk_level: str,
) -> dict[str, Any]:
    return {
        "encounter_id": int(encounter_id),
        "patient_nbr": int(patient_nbr) if patient_nbr is not None else None,
        "readmission_probability": round(float(readmission_probability), 6),
        "risk_level": str(risk_level),
    }


def publish_prediction_message(
    message: dict[str, Any],
    topic: str = KAFKA_PREDICTION_TOPIC,
) -> None:
    producer = create_kafka_sink_producer()
    try:
        publish_json_message(
            producer=producer,
            topic=topic,
            key=str(message["encounter_id"]),
            payload=message,
        )
        logger.info("Published prediction for encounter_id=%s", message["encounter_id"])
    finally:
        producer.close()