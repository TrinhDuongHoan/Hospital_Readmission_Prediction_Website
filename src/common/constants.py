from __future__ import annotations

# =========================
# Paths
# =========================
RAW_DATA_PATH = "data/raw/diabetic_data.csv"
MODEL_DIR = "artifacts/models"
METRICS_DIR = "artifacts/metrics"
LOG_DIR = "artifacts/logs"
DEFAULT_MODEL_PATH = f"{MODEL_DIR}/logistic_baseline.joblib"

# =========================
# Kafka
# =========================
KAFKA_BOOTSTRAP_SERVERS = "127.0.0.1:9092"
KAFKA_INPUT_TOPIC = "hospital-events"
KAFKA_PREDICTION_TOPIC = "hospital-predictions"

# =========================
# Missing values
# =========================
MISSING_VALUES = ["?", "None", "NULL", "null", "NA", "N/A", ""]

# =========================
# Model / features
# =========================
TARGET_COLUMN = "readmitted"
TARGET_BINARY_COLUMN = "target"

DROP_COLUMNS = [
    "encounter_id",
    "patient_nbr",
    "weight",
    "payer_code",
]

HIGH_MISSING_DROP_COLUMNS = [
    "max_glu_serum",
    "A1Cresult",
]

DIAG_COLUMNS = ["diag_1", "diag_2", "diag_3"]

SELECTED_FEATURES = [
    "race",
    "gender",
    "age",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
    "medical_specialty",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "diag_1",
    "diag_2",
    "diag_3",
    "number_diagnoses",
    "change",
    "diabetesMed",
]

CATEGORICAL_FEATURES = [
    "race",
    "gender",
    "age",
    "medical_specialty",
    "diag_1",
    "diag_2",
    "diag_3",
    "change",
    "diabetesMed",
]

NUMERIC_FEATURES = [
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
]

RISK_LABELS = {
    "high_threshold": 0.7,
    "medium_threshold": 0.4,
}