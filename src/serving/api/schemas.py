from pydantic import BaseModel


class PredictionRequest(BaseModel):
    race: str
    gender: str
    age: str
    admission_type_id: int
    discharge_disposition_id: int
    admission_source_id: int
    time_in_hospital: int
    medical_specialty: str
    num_lab_procedures: int
    num_procedures: int
    num_medications: int
    number_outpatient: int
    number_emergency: int
    number_inpatient: int
    diag_1: str
    diag_2: str
    diag_3: str
    number_diagnoses: int
    change: str
    diabetesMed: str


class PredictionResponse(BaseModel):
    readmission_probability: float
    risk_level: str