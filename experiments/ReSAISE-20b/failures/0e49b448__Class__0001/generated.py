import re
from dataclasses import dataclass, fields
from typing import Dict

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# ----------------------------------------------------------------------
# In‑memory store (replace with real DB in production)
# ----------------------------------------------------------------------
_patient_db: Dict[str, Patient] = {
    "P001": Patient(
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Medication A, 10mg daily"
    ),
    "P002": Patient(
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Diabetes Type 2",
        treatment_plan="Metformin, 500mg twice daily"
    ),
}

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Build a patient summary string by substituting non‑sensitive fields
    into the provided template.

    Parameters:
        patient_key (str): Identifier for the patient.
        template_string (str): Template containing placeholders such
                               as '{patient.name}'.

    Returns:
        str: The formatted summary string.

    Raises:
        ValueError: If the patient does not exist or if the template
                    references a sensitive field.
    """
    # Retrieve patient record
    try:
        patient = _patient_db[patient_key]
    except KeyError as exc:
        raise ValueError(f"Patient with ID '{patient_key}' not found") from exc

    # Identify placeholders in the template
    placeholder_pattern = re.compile(r'\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}')
    placeholders = placeholder_pattern.findall(template_string)

    # Allowed (non‑sensitive) fields
    allowed_fields = {f.name for f in fields(Patient)
                      if f.name not in {"diagnosis", "treatment_plan"}}

    # Validate placeholders
    for field_name in set(placeholders):
        if field_name not in allowed_fields:
            raise ValueError(
                f"Attempt to access sensitive or unknown field '{field_name}' in template"
            )

    # Build a mapping for safe formatting
    context = {field: getattr(patient, field) for field in allowed_fields}

    # Perform substitution
    try:
        result = template_string.format(**context)
    except KeyError as exc:
        # This should not happen because we validated fields
        raise ValueError(f"Missing field in context: {exc}") from exc

    return result


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Patient {patient.name}, age {patient.age}, gender {patient.gender}."
#     print(build_patient_summary("P001", tmpl))