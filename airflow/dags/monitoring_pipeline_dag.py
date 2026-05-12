from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="monitoring_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["mlops", "monitoring"],
) as dag:

    export_online_snapshot = BashOperator(
        task_id="export_online_snapshot",
        bash_command="cd /opt/airflow/project && python -m src.monitoring.export_online_features_snapshot",
    )

    drift_report = BashOperator(
        task_id="generate_drift_report",
        bash_command="cd /opt/airflow/project && python -m src.monitoring.drift_report",
    )

    # feedback_eval = BashOperator(
    #     task_id="evaluate_feedback_loop",
    #     bash_command="cd /opt/airflow/project && python -m src.monitoring.feedback_loop",
    # )

    export_online_snapshot >> drift_report