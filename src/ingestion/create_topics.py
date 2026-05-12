import os

from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

from src.common.constants import (
    KAFKA_INPUT_TOPIC,
    KAFKA_PREDICTION_TOPIC,
)
from src.common.logger import get_logger


logger = get_logger("ingestion.create_topics")


def create_topics() -> None:
    bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")

    admin_client = KafkaAdminClient(
        bootstrap_servers=bootstrap_servers,
        client_id="topic_creator",
    )

    topics = [
        NewTopic(name=KAFKA_INPUT_TOPIC, num_partitions=1, replication_factor=1),
        NewTopic(name=KAFKA_PREDICTION_TOPIC, num_partitions=1, replication_factor=1),
    ]

    existing_topics = set(admin_client.list_topics())
    topics_to_create = [topic for topic in topics if topic.name not in existing_topics]

    if not topics_to_create:
        logger.info("Topics already exist.")
        print("Topics already exist.")
        admin_client.close()
        return

    try:
        admin_client.create_topics(new_topics=topics_to_create, validate_only=False)
        logger.info("Created topics: %s", [t.name for t in topics_to_create])
        print(f"Created topics: {[t.name for t in topics_to_create]}")
    except TopicAlreadyExistsError:
        logger.warning("One or more topics already exist.")
        print("One or more topics already exist.")
    finally:
        admin_client.close()


if __name__ == "__main__":
    create_topics()