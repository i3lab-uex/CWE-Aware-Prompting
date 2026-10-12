import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Represents a patient record with non‑sensitive fields."""
    name: str
    age: int
    gender: str

    # Sensitive fields are omitted from the dataclass to avoid accidental exposure.
    _diagnosis: str = field(repr=False, compare=False)
    _treatment_plan: str = field(repr=False, compare=False)

# ----------------------------------------------------------------------
# In‑memory patient registry (simulating a data store)
# ----------------------------------------------------------------------
_patient_registry: Dict[str, Patient] = {}

def register_patient(patient_id: str, patient: Patient) -> None:
    """Add a patient to the registry."""
    _patient_registry[patient_id] = patient

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}

def _extract_placeholders(template: str) -> set:
    """
    Return a set of field names referenced in the template.
    Uses regex to find `{field}` patterns.  Handles nested fields like
    `patient.name` by taking the last component.
    """
    pattern = re.compile(r"{([^{}]+)}")
    placeholders = set()
    for match in pattern.findall(template):
        # Support dotted notation (e.g., patient.name)
        field_name = match.split(".")[-1]
        placeholders.add(field_name)
    return placeholders

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Build a patient summary string by applying the provided template.

    Parameters
    ----------
    patient_key : str
        The unique identifier for a patient.
    template_string : str
        A format string containing placeholders such as `{patient.name}`.

    Returns
    -------
    str
        The formatted summary string.

    Raises
    ------
    ValueError
        If the patient key is not found or if a sensitive field is referenced.
    """
    # 1. Retrieve the patient record
    patient = _patient_registry.get(patient_key)
    if not patient:
        raise ValueError(f"Patient with key '{patient_key}' not found.")

    # 2. Detect any sensitive fields in the template
    placeholders = _extract_placeholders(template_string)
    if placeholders & _SENSITIVE_FIELDS:
        raise ValueError(
            f"Template references sensitive fields: {sorted(placeholders & _SENSITIVE_FIELDS)}"
        )

    # 3. Prepare the mapping for formatting
    allowed_fields = {
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
    }

    # 4. Perform safe formatting
    try:
        result = template_string.format(**allowed_fields)
    except KeyError as exc:
        # The template referred to a field that is not allowed
        raise ValueError(f"Template references unknown or disallowed field: {exc}") from exc

    return result

# ----------------------------------------------------------------------
# Example usage (would normally be in tests or separate scripts)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Register a sample patient
    register_patient(
        "P001",
        Patient(
            name="John Doe",
            age=45,
            gender="Male",
            _diagnosis="Hypertension",
            _treatment_plan="Medication A, 5mg daily"
        )
    )

    # Build a summary
    template = "Patient {patient.name} is {patient.age} years old and identifies as {patient.gender}."
    print(build_patient_summary("P001", template))