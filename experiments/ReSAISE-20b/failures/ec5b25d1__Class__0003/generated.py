import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Patient data model (non‑sensitive fields only)
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    patient_code: str
    name: str
    age: int
    gender: str
    # Sensitive fields are omitted from this dataclass to enforce privacy.
    # In a real system these would be stored separately and protected.

# ------------------------------------------------------------------
# Sample in‑memory patient repository
# ------------------------------------------------------------------
_patient_db: Dict[str, Patient] = {
    "P001": Patient(patient_code="P001", name="Alice Smith", age=30, gender="F"),
    "P002": Patient(patient_code="P002", name="Bob Jones", age=45, gender="M"),
    # ... more patients ...
}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}

def _extract_placeholders(template: str) -> set:
    """
    Return a set of placeholder names found in the template.
    Placeholders are expected to be in the form {patient.<field>}.
    """
    pattern = r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return set(re.findall(pattern, template))

def _get_patient(patient_code: str) -> Patient:
    """
    Retrieve a patient from the repository or raise ValueError.
    """
    patient = _patient_db.get(patient_code)
    if not patient:
        raise ValueError(f"Patient with code '{patient_code}' not found.")
    return patient

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Apply a report template to a patient record.

    Parameters
    ----------
    patient_code : str
        The unique identifier of the patient.
    report_template : str
        A template string containing placeholders such as
        '{patient.name}' or '{patient.age}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient is not found or if a sensitive field is referenced.
    """
    # Validate template placeholders for sensitive data
    placeholders = _extract_placeholders(report_template)
    if placeholders & _SENSITIVE_FIELDS:
        raise ValueError(
            f"Template contains sensitive fields: {placeholders & _SENSITIVE_FIELDS}"
        )

    # Retrieve patient record
    patient = _get_patient(patient_code)

    # Prepare mapping for str.format
    context = {"patient": patient}

    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # The template references a field that does not exist
        raise ValueError(f"Invalid placeholder in template: {exc}") from None

    return report