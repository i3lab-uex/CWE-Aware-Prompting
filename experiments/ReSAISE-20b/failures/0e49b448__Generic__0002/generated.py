import re
from dataclasses import dataclass, fields
from typing import Dict

# ------------------------------------------------------------------
# Patient model and in‑memory database (for demonstration purposes)
# ------------------------------------------------------------------

@dataclass
class Patient:
    name: str
    age: int
    gender: str
    diagnosis: str          # sensitive
    treatment_plan: str     # sensitive

# Example in‑memory patient database
PATIENT_DB: Dict[str, Patient] = {
    "patient_001": Patient(
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A"
    ),
    "patient_002": Patient(
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_ALLOWED_PLACEHOLDERS = {
    f"patient.{field.name}" for field in fields(Patient)
    if field.name not in _SENSITIVE_FIELDS
}

_PLACEHOLDER_RE = re.compile(r"{([^}]+)}")

def _extract_placeholders(template: str) -> set[str]:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}

def _patient_to_dict(patient: Patient) -> Dict[str, str]:
    """Return a dictionary of non‑sensitive patient attributes."""
    return {
        f"patient.{field.name}": str(getattr(patient, field.name))
        for field in fields(Patient)
        if field.name not in _SENSITIVE_FIELDS
    }

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Generate a patient summary string by applying the provided template to
    non‑sensitive fields of the patient record.

    Args:
        patient_key: Identifier for the patient.
        template_string: String containing placeholders such as
                         '{patient.name}', '{patient.age}'.

    Returns:
        A formatted string with the patient's non‑sensitive information.

    Raises:
        ValueError: If the patient key is not found or if the template
                    attempts to access a sensitive field.
    """
    # 1. Retrieve patient record
    patient = PATIENT_DB.get(patient_key)
    if not patient:
        raise ValueError(f"Patient ID '{patient_key}' not found.")

    # 2. Validate placeholders
    placeholders = _extract_placeholders(template_string)
    for ph in placeholders:
        if ph not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(
                f"Attempt to access disallowed or unknown placeholder '{ph}'."
            )

    # 3. Build mapping for format
    mapping = _patient_to_dict(patient)

    # 4. Perform substitution safely
    try:
        result = template_string.format(**mapping)
    except KeyError as exc:
        # This should not happen due to earlier validation
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return result