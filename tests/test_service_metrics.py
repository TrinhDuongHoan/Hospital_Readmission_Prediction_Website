from src.monitoring.service_metrics import ServiceMetrics


def test_service_metrics_record(tmp_path):
    metrics_path = tmp_path / "metrics.json"
    tracker = ServiceMetrics(str(metrics_path))

    tracker.record_prediction("medium", 12.5)
    tracker.record_prediction("high", 8.3)

    summary = tracker.summary()

    assert summary["prediction_count"] == 2
    assert summary["risk_level_counts"]["medium"] == 1
    assert summary["risk_level_counts"]["high"] == 1