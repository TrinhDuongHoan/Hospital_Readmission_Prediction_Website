from src.common.logger import get_logger
from src.orchestration.jobs.backfill_features import run_backfill_features_job
from src.orchestration.jobs.retrain_job import run_retrain_job


logger = get_logger(
    "orchestration.training_pipeline",
    log_file="artifacts/logs/training_pipeline.log",
)


def run_training_pipeline() -> None:
    logger.info("Training pipeline started")

    run_backfill_features_job()
    run_retrain_job()

    logger.info("Training pipeline completed successfully")


if __name__ == "__main__":
    run_training_pipeline()