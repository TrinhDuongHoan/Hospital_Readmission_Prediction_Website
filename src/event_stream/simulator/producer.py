import json
from kafka import KafkaProducer


def create_producer(bootstrap_servers: str = "localhost:9092") -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        key_serializer=lambda k: str(k).encode("utf-8") if k is not None else None,
    )
    return producer


def send_event(producer: KafkaProducer, topic: str, key: str, event: dict) -> None:
    producer.send(topic, key=key, value=event)
    producer.flush()