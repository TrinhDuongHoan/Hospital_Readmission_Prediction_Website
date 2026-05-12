from src.features.mappings import (
    diagnosis_to_group,
    normalize_change,
    normalize_diabetes_med,
    normalize_gender,
)


def test_normalize_gender():
    assert normalize_gender("male") == "Male"
    assert normalize_gender("female") == "Female"
    assert normalize_gender("unknown") == "Unknown"


def test_normalize_change():
    assert normalize_change("Ch") == "Ch"
    assert normalize_change("No") == "No"


def test_normalize_diabetes_med():
    assert normalize_diabetes_med("Yes") == "Yes"
    assert normalize_diabetes_med("No") == "No"


def test_diagnosis_to_group():
    assert diagnosis_to_group("250.8") == "diabetes"
    assert diagnosis_to_group("428") == "circulatory"
    assert diagnosis_to_group("786") == "respiratory"