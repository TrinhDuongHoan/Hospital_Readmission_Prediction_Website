import subprocess
from typing import List

from src.common.logger import get_logger


logger = get_logger(
    "orchestration.streaming_pipeline",
    log_file="artifacts/logs/streaming_pipeline.log",
)


def build_streaming_commands() -> List[List[str]]:
    return [
        ["bash", "scripts/create_topics.sh"],
        ["bash", "scripts/run_stream_predict_to_kafka.sh"],
        ["bash", "scripts/run_simulator.sh"],
    ]


def run_streaming_pipeline(dry_run: bool = True) -> None:
    """
    dry_run=True:
        chỉ in ra lệnh để tránh spawn nhiều process blocking trong local demo.

    dry_run=False:
        sẽ thực thi tuần tự từng lệnh.
    """
    logger.info("Streaming pipeline started | dry_run=%s", dry_run)

    commands = build_streaming_commands()

    for cmd in commands:
        logger.info("Pipeline step: %s", " ".join(cmd))

        if dry_run:
            print("DRY RUN:", " ".join(cmd))
            continue

        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info("stdout:\n%s", result.stdout)
        if result.stderr:
            logger.warning("stderr:\n%s", result.stderr)

    logger.info("Streaming pipeline finished")


if __name__ == "__main__":
    run_streaming_pipeline(dry_run=True)