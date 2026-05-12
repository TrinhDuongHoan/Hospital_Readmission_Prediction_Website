from datetime import datetime, timedelta
import pandas as pd

from src.common.utils import safe_value, safe_int


def build_events_from_row(row: pd.Series) -> list[dict]:
    encounter_id = safe_int(row["encounter_id"])
    patient_nbr = safe_int(row["patient_nbr"])

    base_time = datetime.now()

    admission_event = {
        "event_type": "admission",
        "event_time": (base_time).isoformat(),
        "encounter_id": encounter_id,
        "patient_nbr": patient_nbr,
        "race": str(safe_value(row["race"])),
        "gender": str(safe_value(row["gender"])),
        "age": str(safe_value(row["age"])),
        "admission_type_id": int(row["admission_type_id"]),
        "admission_source_id": int(row["admission_source_id"]),
        "medical_specialty": str(safe_value(row["medical_specialty"])),
        "diag_1": str(safe_value(row["diag_1"])),
        "diag_2": str(safe_value(row["diag_2"])),
        "diag_3": str(safe_value(row["diag_3"])),
    }

    lab_event = {
        "event_type": "lab_result",
        "event_time": (base_time + timedelta(minutes=5)).isoformat(),
        "encounter_id": encounter_id,
        "patient_nbr": patient_nbr,
        "num_lab_procedures": int(row["num_lab_procedures"]),
        "max_glu_serum": str(safe_value(row["max_glu_serum"])),
        "A1Cresult": str(safe_value(row["A1Cresult"])),
        "number_diagnoses": int(row["number_diagnoses"]),
    }

    medication_event = {
        "event_type": "medication_update",
        "event_time": (base_time + timedelta(minutes=10)).isoformat(),
        "encounter_id": encounter_id,
        "patient_nbr": patient_nbr,
        "num_medications": int(row["num_medications"]),
        "change": str(safe_value(row["change"])),
        "diabetesMed": str(safe_value(row["diabetesMed"])),
    }

    discharge_event = {
        "event_type": "discharge",
        "event_time": (base_time + timedelta(minutes=15)).isoformat(),
        "encounter_id": encounter_id,
        "patient_nbr": patient_nbr,
        "discharge_disposition_id": int(row["discharge_disposition_id"]),
        "time_in_hospital": int(row["time_in_hospital"]),
        "num_procedures": int(row["num_procedures"]),
        "number_outpatient": int(row["number_outpatient"]),
        "number_emergency": int(row["number_emergency"]),
        "number_inpatient": int(row["number_inpatient"]),
    }

    return [admission_event, lab_event, medication_event, discharge_event]