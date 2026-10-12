import re
from dataclasses import dataclass, fields
from typing import Dict

# -------------------------------------------------------------
# Patient data model (non‑sensitive only)
# -------------------------------------------------------------
@dataclass
class Patient:
    code: str          # unique identifier
    name: str
    age: int
    gender: str

# Sensitive fields are intentionally omitted from the dataclass.
# In a real system these would be stored separately and protected.

# -------------------------------------------------------------
# In‑memory patient database (for demo purposes)
# -------------------------------------------------------------
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(code="P001", name="Alice Smith", age=30, gender="F"),
    "P002": Patient(code="P002", name="Bob Jones", age=45, gender="M"),
    # ... add more patients as needed
}

# -------------------------------------------------------------
# Helper utilities
# -------------------------------------------------------------
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}

_PLACEHOLDER_REGEX = re.compile(r"{([^{}]+)}")

def _extract_placeholders(template: str) -> set:
    """
    Return a set of placeholder names found in the template.
    Example: "Hello {patient.name}, age {patient.age}" ->
             {"patient.name", "patient.age"}
    """
    return set(match.group(1).strip() for match in _PLACEHOLDER_REGEX.finditer(template))

def _validate_placeholders(placeholders: set):
    """
    Ensure no sensitive data is requested and all placeholders
    refer to allowed attributes of Patient.
    """
    for ph in placeholders:
        # Expect format 'patient.attribute'
        if not ph.startswith("patient."):
            raise ValueError(f"Unsupported placeholder: {ph}")

        attr = ph.split(".", 1)[1]
        if attr in _SENSITIVE_FIELDS:
            raise ValueError(f"Attempt to access sensitive information: {attr}")

        # Ensure attribute exists on Patient
        if not any(f.name == attr for f in fields(Patient)):
            raise ValueError(f"Unknown patient attribute: {attr}")

def _format_patient_info(patient: Patient, template: str) -> str:
    """
    Safely format the template using only patient attributes.
    """
    # Build a dict of allowed values
    data = {f.name: getattr(patient, f.name) for f in fields(Patient)}
    try:
        return template.format(**{"patient": data})
    except KeyError as exc:
        raise ValueError(f"Missing placeholder value: {exc}") from None
    except Exception as exc:
        raise ValueError(f"Error formatting template: {exc}") from None

# -------------------------------------------------------------
# Public API
# -------------------------------------------------------------
def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient report string based on the provided template.

    Parameters
    ----------
    patient_code : str
        The unique identifier of the patient.
    report_template : str
        A template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string containing only non‑sensitive patient data.

    Raises
    ------
    ValueError
        If the patient ID is not found, or if the template attempts to
        access sensitive information or unknown attributes.
    """
    # Validate input types
    if not isinstance(patient_code, str) or not isinstance(report_template, str):
        raise ValueError("Both patient_code and report_template must be strings.")

    # Retrieve patient
    patient = _PATIENT_DB.get(patient_code)
    if not patient:
        raise ValueError(f"Patient with code '{patient_code}' not found.")

    # Extract and validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # Format and return the report
    return _format_patient_info(patient, report_template)