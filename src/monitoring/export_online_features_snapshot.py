from pathlib import Path
import pandas as pd

from src.common.logger import get_logger


logger = get_logger("monitoring.export_online_snapshot")


def export_online_snapshot(
    source_path: str = "artifacts/logs/online_feature_store.json",
    output_path: str = "artifacts/logs/latest_online_features.csv",
) -> str:
    src = Path(source_path)
    if not src.exists():
        raise FileNotFoundError(f"Online feature store file not found: {source_path}")

    df = pd.read_json(src).T
    df.reset_index(drop=True, inplace=True)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)

    logger.info("Exported online feature snapshot to %s", output_path)
    return str(output)


def main():
    output_path = export_online_snapshot()
    print(f"Saved snapshot to {output_path}")


if __name__ == "__main__":
    main()