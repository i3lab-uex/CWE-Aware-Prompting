import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Domain model and in‑memory data store (for demo purposes)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str
    # any other attributes can be added here

# Example patient repository – in a real system this would query a DB
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, monitor blood pressure daily"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Metformin, diet and exercise"
    ),
}

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
_ALLOWED_PATIENT_FIELDS = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan",
}

_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _get_patient_by_id(patient_id: str) -> Patient:
    """Retrieve a patient from the repository, raising ValueError if not found."""
    patient = _PATIENT_DB.get(patient_id)
    if patient is None:
        raise ValueError(f"Patient ID '{patient_id}' does not exist.")
    return patient

def _replace_placeholders(template: str, patient: Patient) -> str:
    """
    Replace placeholders of the form {patient.<field>} with the actual value.
    Raises ValueError if an unsupported field is requested.
    """
    def repl(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in _ALLOWED_PATIENT_FIELDS:
            raise ValueError(f"Access to restricted or unknown field '{field_name}'.")
        value = getattr(patient, field_name)
        return str(value)

    # Perform substitution
    result = _PLACEHOLDER_RE.sub(repl, template)

    # After substitution check that no unreplaced placeholders remain
    if _PLACEHOLDER_RE.search(result):
        raise ValueError("Template contains invalid or unsupported placeholders.")
    return result

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by filling in the provided template.

    Parameters
    ----------
    patient_id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders like {patient.name}.

    Returns
    -------
    str
        The rendered summary string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if a placeholder references
        restricted or unknown data.
    """
    # 1. Retrieve patient record (validates ID)
    patient = _get_patient_by_id(patient_id)

    # 2. Replace placeholders securely
    summary = _replace_placeholders(report_template, patient)

    return summary

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Patient Report:\n"
#         "Name: {patient.name}\n"
#         "Age: {patient.age}\n"
#         "Gender: {patient.gender}\n"
#         "Diagnosis: {patient.diagnosis}\n"
#         "Treatment Plan: {patient.treatment_plan}"
#     )
#     print(generate_patient_summary("P001", template))