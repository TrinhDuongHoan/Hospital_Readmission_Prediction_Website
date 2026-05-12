import json
from pathlib import Path
from time import perf_counter
from typing import Any


class ServiceMetrics:
    def __init__(self, output_path: str = "artifacts/logs/service_metrics.json"):
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.metrics = {
            "prediction_count": 0,
            "risk_level_counts": {
                "low": 0,
                "medium": 0,
                "high": 0,
            },
            "latency_ms": [],
        }
        self._write()

    def _write(self) -> None:
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)

    def record_prediction(self, risk_level: str, latency_ms: float | None = None) -> None:
        self.metrics["prediction_count"] += 1

        if risk_level not in self.metrics["risk_level_counts"]:
            self.metrics["risk_level_counts"][risk_level] = 0

        self.metrics["risk_level_counts"][risk_level] += 1

        if latency_ms is not None:
            self.metrics["latency_ms"].append(round(float(latency_ms), 3))

        self._write()

    def summary(self) -> dict[str, Any]:
        latencies = self.metrics["latency_ms"]
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0

        return {
            "prediction_count": self.metrics["prediction_count"],
            "risk_level_counts": self.metrics["risk_level_counts"],
            "avg_latency_ms": round(avg_latency, 3),
        }


class Timer:
    def __enter__(self):
        self.start = perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = perf_counter()
        self.elapsed_ms = (self.end - self.start) * 1000.0