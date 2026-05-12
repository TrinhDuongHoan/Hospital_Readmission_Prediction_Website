from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="training_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "training"],
) as dag:

    backfill_features = BashOperator(
        task_id="backfill_offline_features",
        bash_command="cd /opt/airflow/project && python -m src.features.offline.build_offline_features",
    )

    train_model = BashOperator(
        task_id="train_model",
        bash_command="cd /opt/airflow/project && python -m src.training.train",
    )

    evaluate_model = BashOperator(
        task_id="evaluate_model",
        bash_command="cd /opt/airflow/project && python -m src.training.evaluate",
    )

    backfill_features >> train_model >> evaluate_model