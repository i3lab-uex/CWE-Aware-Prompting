import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------
# Domain model and in‑memory store
# ------------------------------

@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    # Sensitive fields – should never be exposed via compose_patient_report
    diagnosis: str
    treatment_plan: str

# In‑memory patient repository (for demo purposes)
_PATIENT_DB: Dict[str, Patient] = {
    "123": Patient(
        uid="123",
        name="John Doe",
        age=45,
        gender="M",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "456": Patient(
        uid="456",
        name="Jane Smith",
        age=30,
        gender="F",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ------------------------------
# Helper utilities
# ------------------------------

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_ALLOWED_PLACEHOLDERS_RE = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _extract_placeholders(template: str) -> set:
    """
    Return a set of placeholder names found in the template.
    Only placeholders matching {patient.<field>} are considered valid.
    """
    return set(match.group(1) for match in _ALLOWED_PLACEHOLDERS_RE.finditer(template))

def _validate_placeholders(placeholders: set) -> None:
    """
    Ensure that none of the placeholders refer to sensitive fields.
    Raise ValueError if a sensitive field is requested.
    """
    for field in placeholders:
        if field in _SENSITIVE_FIELDS:
            raise ValueError(f"Attempt to expose sensitive patient data: '{field}'")

def _format_template(template: str, patient: Patient) -> str:
    """
    Safely format the template using only allowed attributes of the patient.
    """
    # Build a mapping from placeholder names to values
    data = {field: getattr(patient, field) for field in _extract_placeholders(template)}
    # Use Python's format method with the mapping
    try:
        return template.format(patient=data)
    except KeyError as exc:
        # This should not happen if placeholders were extracted correctly
        raise ValueError(f"Missing patient attribute: {exc}") from exc

# ------------------------------
# Public API
# ------------------------------

def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report string based on the provided template.

    Parameters
    ----------
    patient_uid : str
        The unique identifier of the patient.
    report_schema : str
        Template string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string containing only non-sensitive patient data.

    Raises
    ------
    ValueError
        If the patient UID does not exist, or if the template attempts to
        expose sensitive information (diagnosis or treatment_plan).
    """
    # 1. Retrieve patient
    patient = _PATIENT_DB.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found")

    # 2. Extract and validate placeholders
    placeholders = _extract_placeholders(report_schema)
    _validate_placeholders(placeholders)

    # 3. Format and return the report
    return _format_template(report_schema, patient)

# ------------------------------
# Example usage (for testing)
# ------------------------------

if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}"
    )
    print(compose_patient_report("123", template))