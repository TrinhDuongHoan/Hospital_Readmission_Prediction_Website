from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="backfill_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["mlops", "ops"],
) as dag:

    create_topics = BashOperator(
        task_id="create_topics",
        bash_command="cd /opt/airflow/project && python -m src.ingestion.create_topics",
    )

    build_features = BashOperator(
        task_id="build_offline_features",
        bash_command="cd /opt/airflow/project && python -m src.features.offline.build_offline_features ",
    )

    create_topics >> build_features