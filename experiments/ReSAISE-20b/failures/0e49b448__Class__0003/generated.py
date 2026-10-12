import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------
# Patient model and in‑memory registry (for demonstration purposes)
# --------------------------------------------------------------------

@dataclass
class Patient:
    patient_key: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# Simple in‑memory patient registry.
PATIENT_REGISTRY: Dict[str, Patient] = {}

def add_patient(patient: Patient) -> None:
    """Adds a patient to the registry."""
    PATIENT_REGISTRY[patient.patient_key] = patient

# --------------------------------------------------------------------
# Utility functions
# --------------------------------------------------------------------

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _validate_template(template: str) -> None:
    """Ensure that the template does not request sensitive data."""
    for match in _PLACEHOLDER_RE.finditer(template):
        field_name = match.group(1)
        if field_name in _SENSITIVE_FIELDS:
            raise ValueError(f"Attempt to access sensitive field '{field_name}' in template")

def _substitute(patient: Patient, template: str) -> str:
    """Replace placeholders with patient attribute values."""
    def repl(match):
        field_name = match.group(1)
        # Use getattr; if attribute missing raise KeyError -> ValueError
        try:
            value = getattr(patient, field_name)
        except AttributeError as exc:
            raise ValueError(f"Field '{field_name}' does not exist in patient data") from exc
        return str(value)

    return _PLACEHOLDER_RE.sub(repl, template)

# --------------------------------------------------------------------
# Main API
# --------------------------------------------------------------------

def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Build a non‑sensitive patient summary from the provided template.

    Parameters
    ----------
    patient_key : str
        The unique identifier for the patient.
    template_string : str
        A string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The populated summary string.

    Raises
    ------
    ValueError
        If the patient does not exist or if the template tries to access
        sensitive fields (diagnosis, treatment_plan).
    """
    # 1. Retrieve patient record
    patient = PATIENT_REGISTRY.get(patient_key)
    if not patient:
        raise ValueError(f"Patient with key '{patient_key}' not found")

    # 2. Validate template does not request sensitive data
    _validate_template(template_string)

    # 3. Substitute placeholders
    return _substitute(patient, template_string)

# --------------------------------------------------------------------
# Example usage (for testing purposes)
# --------------------------------------------------------------------

if __name__ == "__main__":
    # Create and register a patient
    p = Patient(
        patient_key="12345",
        name="John Doe",
        age=42,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A"
    )
    add_patient(p)

    # Build a safe summary
    tmpl = "Patient {patient.name} (age {patient.age}) is {patient.gender}."
    print(build_patient_summary("12345", tmpl))

    # Attempting to access sensitive data raises an error
    bad_tmpl = "Diagnosis: {patient.diagnosis}"
    try:
        build_patient_summary("12345", bad_tmpl)
    except ValueError as e:
        print(f"Error: {e}")