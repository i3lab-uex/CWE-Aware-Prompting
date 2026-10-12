import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Mock database and helper functions (replace with real DB logic)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive data
    treatment_plan: str     # Sensitive data

# In‑memory patient store for demonstration purposes.
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, Regular check‑ups"
    ),
}

def get_patient_by_id(patient_id: str) -> Patient:
    """Retrieve a patient record by ID."""
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")
    return patient

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Generate a personalized patient report by substituting placeholders
    in the provided template with actual patient data.

    Parameters:
        patient_identifier (str): Unique ID of the patient.
        report_template (str): Template string containing placeholders
                               like '{patient.name}', '{patient.age}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the patient ID is invalid or if restricted
                    medical information is accessed.
    """
    # Retrieve patient record; raises ValueError if ID invalid
    patient = get_patient_by_id(patient_identifier)

    # Convert the Patient dataclass to a dictionary for formatting
    patient_dict = asdict(patient)

    # Define which fields are allowed to be exposed in reports.
    # Sensitive fields (diagnosis, treatment_plan) are disallowed unless
    # explicitly whitelisted by the caller. Here we enforce restriction.
    allowed_fields = {"name", "age", "gender"}

    # Find all placeholders in the template.
    placeholder_pattern = r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}"
    placeholders = re.findall(placeholder_pattern, report_template)

    # Validate each placeholder.
    for field in placeholders:
        if field not in patient_dict:
            raise ValueError(f"Unknown placeholder: {{patient.{field}}}")
        if field not in allowed_fields:
            raise ValueError(
                f"Access to restricted patient information '{field}' is not allowed."
            )

    # Prepare the mapping for str.format
    format_map = {"patient": patient_dict}

    try:
        report = report_template.format(**format_map)
    except KeyError as exc:
        # This should not happen due to prior validation, but guard anyway.
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report