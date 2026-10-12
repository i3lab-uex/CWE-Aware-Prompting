import re
from typing import Dict

# --- Mock patient database and retrieval function ---------------------------------
class Patient:
    """
    A simple data holder for patient information.
    In a real system this would be replaced by an ORM model or database access layer.
    """
    def __init__(self, identifier: str, name: str, age: int, gender: str,
                 diagnosis: str, treatment_plan: str):
        self.identifier = identifier
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis          # Sensitive data
        self.treatment_plan = treatment_plan  # Sensitive data

# Simulated in‑memory database
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient("P001", "Alice Smith", 30, "F",
                    "Hypertension", "Lifestyle changes and medication"),
    "P002": Patient("P002", "Bob Johnson", 45, "M",
                    "Type II Diabetes", "Insulin therapy"),
}

def _get_patient_by_id(identifier: str) -> Patient:
    """
    Retrieve a patient object from the simulated database.
    Raises ValueError if the identifier is unknown.
    """
    patient = _PATIENT_DB.get(identifier)
    if not patient:
        raise ValueError(f"Patient ID '{identifier}' does not exist.")
    return patient

# --- Core functionality ----------------------------------------------------------
_ALLOWED_FIELDS = {
    "patient.name",
    "patient.age",
    "patient.gender"
}

# Regex to find placeholders like {patient.name}
_PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_.]+)\}")

def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Build a patient summary by substituting placeholders in the report template.

    Parameters
    ----------
    identifier : str
        The unique patient identifier.
    report_template : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report with placeholders replaced by actual patient data.

    Raises
    ------
    ValueError
        If the identifier is invalid or if a placeholder refers to restricted data.
    """
    # Retrieve patient record
    patient = _get_patient_by_id(identifier)

    # Find all placeholders in the template
    placeholders = set(_PLACEHOLDER_RE.findall(report_template))

    # Validate placeholders against allowed fields
    for ph in placeholders:
        if ph not in _ALLOWED_FIELDS:
            raise ValueError(f"Access to '{ph}' is restricted or invalid.")

    # Build a mapping for format()
    values = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender
    }

    # Perform substitution safely
    try:
        formatted_report = report_template.format(**values)
    except KeyError as exc:
        # This should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing value for placeholder {exc}") from exc

    return formatted_report