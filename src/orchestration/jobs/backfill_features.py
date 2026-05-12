import subprocess

from src.common.logger import get_logger


logger = get_logger(
    "orchestration.backfill_features",
    log_file="artifacts/logs/backfill_features.log",
)


def run_backfill_features_job() -> None:
    logger.info("Starting backfill feature job")

    cmd = ["python", "-m", "src.features.offline.build_offline_features"]
    logger.info("Running command: %s", " ".join(cmd))

    result = subprocess.run(cmd, check=True, capture_output=True, text=True)

    logger.info("stdout:\n%s", result.stdout)
    if result.stderr:
        logger.warning("stderr:\n%s", result.stderr)

    logger.info("Backfill feature job completed successfully")


if __name__ == "__main__":
    run_backfill_features_job()