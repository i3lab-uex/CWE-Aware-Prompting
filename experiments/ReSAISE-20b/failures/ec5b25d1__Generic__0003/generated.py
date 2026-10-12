import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------
# Patient model and in‑memory store
# --------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """A simple patient record containing non‑sensitive data."""
    code: str
    name: str
    age: int
    gender: str
    # Sensitive fields are omitted from the public API
    _diagnosis: str = ""
    _treatment_plan: str = ""

# In‑memory patient registry (code -> Patient)
PATIENT_REGISTRY: Dict[str, Patient] = {
    "P001": Patient(code="P001", name="Alice Smith", age=29, gender="F",
                    _diagnosis="Hypertension", _treatment_plan="Medication A"),
    "P002": Patient(code="P002", name="Bob Jones", age=45, gender="M",
                    _diagnosis="Diabetes", _treatment_plan="Insulin therapy"),
    # Add more patients as needed
}

# --------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------

# Allowed placeholder fields (non‑sensitive)
ALLOWED_FIELDS = {"name", "age", "gender"}

# Regular expression to find placeholders of the form {patient.<field>}
PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of field names referenced in the template."""
    return set(PLACEHOLDER_RE.findall(template))

def _validate_template(fields: set):
    """Ensure no sensitive fields are referenced."""
    for field in fields:
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Access to sensitive patient field '{field}' is prohibited.")

def _format_patient_data(patient: Patient, template: str) -> str:
    """Perform the actual substitution using a safe mapping."""
    # Convert patient dataclass to dict, exposing only allowed fields
    data = {k: getattr(patient, k) for k in ALLOWED_FIELDS}
    try:
        return template.format(**data)
    except KeyError as exc:
        raise ValueError(f"Template references unknown field: {exc}") from None

# --------------------------------------------------------------
# Public API
# --------------------------------------------------------------

def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient report string based on the provided template.

    Parameters
    ----------
    patient_code : str
        The unique identifier for a patient.
    report_template : str
        A string containing placeholders like '{patient.name}' to be replaced with patient data.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID does not exist, or if the template attempts to access sensitive data.
    """
    # 1. Retrieve patient record
    patient = PATIENT_REGISTRY.get(patient_code)
    if not patient:
        raise ValueError(f"Patient with code '{patient_code}' not found.")

    # 2. Extract and validate placeholders
    fields = _extract_placeholders(report_template)
    _validate_template(fields)

    # 3. Format the template safely
    return _format_patient_data(patient, report_template)

# --------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------

if __name__ == "__main__":
    template = "Patient {patient.name} (age {patient.age}) is a {patient.gender}."
    print(create_person_report("P001", template))