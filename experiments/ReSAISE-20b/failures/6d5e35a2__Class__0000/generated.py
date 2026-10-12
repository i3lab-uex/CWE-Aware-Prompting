import re
from dataclasses import dataclass, asdict
from typing import Dict

# Mock patient data store – in a real system this would be replaced by a database or secure API
_PATIENT_DB: Dict[str, "Patient"] = {}

@dataclass(frozen=True)
class Patient:
    """Represents a patient record with sensitive information."""
    pat_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive information
    treatment_plan: str     # Sensitive information

# Populate the mock database with a few sample patients
_PATIENT_DB["12345"] = Patient(
    pat_id="12345",
    name="John Doe",
    age=42,
    gender="Male",
    diagnosis="Hypertension",
    treatment_plan="Medication: Lisinopril 10mg daily"
)
_PATIENT_DB["67890"] = Patient(
    pat_id="67890",
    name="Jane Smith",
    age=30,
    gender="Female",
    diagnosis="Asthma",
    treatment_plan="Inhaler: Albuterol 2 puffs as needed"
)

# Define which placeholders are considered safe to expose
_SAFE_PLACEHOLDERS = {
    "patient.name",
    "patient.age",
    "patient.gender"
}

# Regular expression to find placeholders in the layout
_PLACEHOLDER_RE = re.compile(r"\{([^\}]+)\}")

def _validate_placeholders(layout: str) -> None:
    """
    Ensure that all placeholders in the layout are allowed.
    Raises ValueError if a restricted placeholder is found.
    """
    for match in _PLACEHOLDER_RE.finditer(layout):
        placeholder = match.group(1).strip()
        if placeholder not in _SAFE_PLACEHOLDERS:
            raise ValueError(f"Access to restricted information '{placeholder}' is not allowed")

def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized patient report by substituting placeholders in the layout
    with actual patient data.

    Args:
        pat_id: The unique identifier of the patient.
        layout: A string containing placeholders such as '{patient.name}'.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the patient ID is invalid or if restricted data is requested.
    """
    # Retrieve patient record
    patient = _PATIENT_DB.get(pat_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {pat_id}")

    # Validate placeholders before substitution
    _validate_placeholders(layout)

    # Build a mapping of allowed fields
    patient_dict = asdict(patient)
    safe_data = {f"patient.{k}": v for k, v in patient_dict.items() if f"patient.{k}" in _SAFE_PLACEHOLDERS}

    # Perform substitution
    try:
        report = layout.format(**safe_data)
    except KeyError as e:
        # This should not happen due to earlier validation, but handle just in case
        raise ValueError(f"Missing placeholder data for {e}") from e

    return report