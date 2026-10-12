import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Data model and in‑memory store (would normally be a database)
# ------------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Highly sensitive
    treatment_plan: str     # Highly sensitive

# Sample patient database (in a real system this would be secure)
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        patient_id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication",
    ),
    "p002": Patient(
        patient_id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy",
    ),
}

# ------------------------------------------------------------------
# Utility helpers
# ------------------------------------------------------------------
_ALLOWED_FIELDS = {"name", "age", "gender"}  # Only these may be exposed

_PLACEHOLDER_REGEX = re.compile(r"\{(?P<path>[^}]+)\}")

def _extract_placeholders(template: str):
    """Return a set of attribute names referenced in the template."""
    return {match.group("path") for match in _PLACEHOLDER_REGEX.finditer(template)}

def _build_mapping(patient: Patient) -> Dict[str, str]:
    """Return a dict mapping allowed placeholders to patient values."""
    return {
        key: getattr(patient, key)
        for key in _ALLOWED_FIELDS
    }

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by filling in placeholders in the template.

    Parameters
    ----------
    patient_id : str
        Unique identifier of the patient.
    report_template : str
        String containing placeholders like '{patient.name}' or '{patient.age}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if the template attempts to access
        restricted data (diagnosis, treatment_plan, etc.).
    """
    # 1. Validate patient existence
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")

    # 2. Validate placeholders
    placeholders = _extract_placeholders(report_template)
    for placeholder in placeholders:
        # Strip any leading "patient." prefix if present
        attr = placeholder.split(".")[-1]
        if attr not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted or unknown attribute '{attr}' is not allowed."
            )

    # 3. Prepare mapping and format
    mapping = _build_mapping(patient)
    try:
        formatted_report = report_template.format(**mapping)
    except KeyError as exc:
        # This should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return formatted_report

# ------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}"
    )
    print(generate_patient_summary("p001", template))