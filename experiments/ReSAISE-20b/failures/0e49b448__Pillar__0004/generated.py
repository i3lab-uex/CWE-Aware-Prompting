import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model and in‑memory storage                                            #
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """Represents a patient record."""
    name: str
    age: int
    gender: str
    # Sensitive fields – must never be exposed through templates
    diagnosis: str = field(repr=False, compare=False)
    treatment_plan: str = field(repr=False, compare=False)

# In‑memory "database" of patients keyed by patient_id
PATIENT_DB: Dict[str, Patient] = {
    "patient_001": Patient(
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "patient_002": Patient(
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Diabetes Type II",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------------- #
# Helper functions                                                             #
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}

def _get_patient(patient_key: str) -> Patient:
    """
    Retrieve a patient from the database.
    Raises ValueError if the key does not exist.
    """
    try:
        return PATIENT_DB[patient_key]
    except KeyError as exc:
        raise ValueError(f"Patient with key '{patient_key}' not found") from exc

def _extract_placeholders(template: str) -> set:
    """
    Return a set of placeholders found in the template.
    Placeholders are expected to be of the form {patient.field}.
    """
    pattern = r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return set(re.findall(pattern, template))

def _validate_placeholders(placeholders: set):
    """
    Ensure that no sensitive fields are referenced in the template.
    Raises ValueError if a forbidden field is found.
    """
    intersection = placeholders & _SENSITIVE_FIELDS
    if intersection:
        raise ValueError(
            f"Template attempts to access sensitive fields: {', '.join(intersection)}"
        )

def _build_context(patient: Patient) -> Dict[str, str]:
    """
    Build a context dictionary mapping field names to string values
    for safe substitution into the template.
    """
    ctx = {}
    for field_name in vars(patient):
        # Skip sensitive fields (they should not appear here, but be safe)
        if field_name in _SENSITIVE_FIELDS:
            continue
        value = getattr(patient, field_name)
        ctx[field_name] = str(value)
    return ctx

# --------------------------------------------------------------------------- #
# Public API                                                                   #
# --------------------------------------------------------------------------- #

def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Generate a patient summary string by substituting placeholders
    in the template with non-sensitive patient data.

    Args:
        patient_key: The identifier of the patient.
        template_string: A string containing placeholders like
                         '{patient.name}', '{patient.age}'.

    Returns:
        A formatted string with the patient's non-sensitive information.

    Raises:
        ValueError: If the patient is not found, or if the template
                    references sensitive fields (diagnosis or treatment_plan).
    """
    # Retrieve patient record
    patient = _get_patient(patient_key)

    # Extract and validate placeholders
    placeholders = _extract_placeholders(template_string)
    _validate_placeholders(placeholders)

    # Build context for substitution
    context = _build_context(patient)

    # Perform safe replacement
    def replacer(match):
        field_name = match.group(1).strip()
        return context.get(field_name, "")

    safe_template = re.sub(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}", replacer, template_string)
    return safe_template

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)                                            #
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = "Patient {patient.name} (Age: {patient.age}) is a {patient.gender}."
#     print(build_patient_summary("patient_001", tmpl))