from typing import Any


def normalize_medical_specialty(value: Any) -> str:
    if value is None:
        return "missing"

    value = str(value).strip()
    if value == "" or value.lower() in {"nan", "none", "null", "missing"}:
        return "missing"

    return value


def normalize_gender(value: Any) -> str:
    if value is None:
        return "Unknown"

    value = str(value).strip()
    if value.lower() in {"male", "m"}:
        return "Male"
    if value.lower() in {"female", "f"}:
        return "Female"
    return "Unknown"


def normalize_change(value: Any) -> str:
    if value is None:
        return "No"

    value = str(value).strip()
    if value.lower() in {"ch", "change"}:
        return "Ch"
    return "No"


def normalize_diabetes_med(value: Any) -> str:
    if value is None:
        return "No"

    value = str(value).strip()
    if value.lower() in {"yes", "y"}:
        return "Yes"
    return "No"


def normalize_age_band(value: Any) -> str:
    if value is None:
        return "missing"
    value = str(value).strip()
    return value if value else "missing"


def diagnosis_to_group(diag_code: Any) -> str:
    """
    Map ICD-9 diagnosis code into coarse disease groups
    similar to the paper-style grouping.
    """
    if diag_code is None:
        return "missing"

    raw = str(diag_code).strip()
    if raw == "" or raw.lower() in {"nan", "none", "null", "missing"}:
        return "missing"

    # strip V / E special groups first
    upper_raw = raw.upper()
    if upper_raw.startswith("V") or upper_raw.startswith("E"):
        return "external_causes"

    try:
        code = float(raw)
    except ValueError:
        return "other"

    if 390 <= code < 460 or code == 785:
        return "circulatory"
    if 460 <= code < 520 or code == 786:
        return "respiratory"
    if 520 <= code < 580 or code == 787:
        return "digestive"
    if int(code) == 250:
        return "diabetes"
    if 800 <= code < 1000:
        return "injury"
    if 710 <= code < 740:
        return "musculoskeletal"
    if 580 <= code < 630 or code == 788:
        return "genitourinary"
    if 140 <= code < 240:
        return "neoplasms"

    return "other"