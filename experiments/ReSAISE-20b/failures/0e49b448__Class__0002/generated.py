import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Minimal patient model used by the reporting system.
# In a real application this would be replaced with the actual ORM or
# domain model implementation.
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    patient_key: str
    name: str
    age: int
    gender: str
    diagnosis: str          # sensitive
    treatment_plan: str     # sensitive

# ----------------------------------------------------------------------
# In-memory patient repository.
# Replace with a real database lookup in production code.
# ----------------------------------------------------------------------
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        patient_key="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "p002": Patient(
        patient_key="p002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, Allergy testing"
    ),
}

# ----------------------------------------------------------------------
# Helper to expose only non-sensitive attributes
# ----------------------------------------------------------------------
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}

def _get_patient(patient_key: str) -> Patient:
    """Retrieve a patient from the repository or raise an error."""
    try:
        return _PATIENT_DB[patient_key]
    except KeyError as exc:
        raise ValueError(f"Patient with key '{patient_key}' not found.") from exc


def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Build a patient summary string based on the supplied template.

    Parameters
    ----------
    patient_key : str
        The unique identifier of the patient.
    template_string : str
        A string containing placeholders in the form '{patient.<field>}'.

    Returns
    -------
    str
        The formatted patient summary string.

    Raises
    ------
    ValueError
        If the patient ID does not exist, or if a placeholder references
        a sensitive field (diagnosis or treatment_plan).
    """
    patient = _get_patient(patient_key)

    # Find all placeholders in the template
    placeholder_pattern = re.compile(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}")
    placeholders = placeholder_pattern.findall(template_string)

    # Validate each placeholder
    for field in set(placeholders):  # use set to avoid duplicate checks
        if field in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field}' is prohibited.")
        if not hasattr(patient, field):
            raise ValueError(f"Patient has no attribute '{field}'.")

    # Prepare a dict of allowed attributes for formatting
    context = {f"patient.{field}": getattr(patient, field) for field in placeholders}

    try:
        result = template_string.format(**context)
    except KeyError as exc:
        # This should not happen because we validated fields above
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return result


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = "Patient {patient.name} ({patient.age} years old, {patient.gender})"
    print(build_patient_summary("p001", tmpl))