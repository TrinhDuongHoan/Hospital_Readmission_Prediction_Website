import json
from typing import Any

from kafka import KafkaProducer

from src.common.constants import KAFKA_BOOTSTRAP_SERVERS
from src.common.logger import get_logger


logger = get_logger(
    "stream.sinks",
    log_file="artifacts/logs/stream_sinks.log",
)


def create_kafka_sink_producer(
    bootstrap_servers: str = KAFKA_BOOTSTRAP_SERVERS,
) -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: str(k).encode("utf-8") if k is not None else None,
    )
    return producer


def publish_json_message(
    producer: KafkaProducer,
    topic: str,
    key: str | None,
    payload: dict[str, Any],
) -> None:
    producer.send(topic, key=key, value=payload)
    producer.flush()
    logger.info("Published message to topic=%s key=%s", topic, key)