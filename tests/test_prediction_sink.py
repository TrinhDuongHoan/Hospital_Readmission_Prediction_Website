from src.event_stream.sinks.prediction_sink import build_prediction_message


def test_build_prediction_message():
    msg = build_prediction_message(
        encounter_id=123,
        patient_nbr=456,
        readmission_probability=0.81234,
        risk_level="high",
    )

    assert msg["encounter_id"] == 123
    assert msg["patient_nbr"] == 456
    assert msg["readmission_probability"] == 0.81234
    assert msg["risk_level"] == "high"