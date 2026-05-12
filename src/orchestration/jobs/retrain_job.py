import subprocess

from src.common.logger import get_logger


logger = get_logger(
    "orchestration.retrain_job",
    log_file="artifacts/logs/retrain_job.log",
)


def run_retrain_job() -> None:
    logger.info("Starting retrain job")

    commands = [
        ["python", "-m", "src.training.train"],
        ["python", "-m", "src.training.evaluate"],
    ]

    for cmd in commands:
        logger.info("Running command: %s", " ".join(cmd))
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("stdout:\n%s", result.stdout)
        if result.stderr:
            logger.warning("stderr:\n%s", result.stderr)

    logger.info("Retrain job completed successfully")


if __name__ == "__main__":
    run_retrain_job()