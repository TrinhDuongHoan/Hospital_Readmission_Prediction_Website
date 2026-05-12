from src.common.utils import risk_to_label, safe_int, normalize_category


def test_risk_to_label():
    assert risk_to_label(0.8) == "high"
    assert risk_to_label(0.5) == "medium"
    assert risk_to_label(0.2) == "low"


def test_safe_int():
    assert safe_int("5") == 5
    assert safe_int(None) == 0
    assert safe_int("abc") == 0


def test_normalize_category():
    assert normalize_category(" Male ") == "Male"
    assert normalize_category(None) == "missing"