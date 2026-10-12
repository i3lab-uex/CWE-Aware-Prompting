import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Mock patient storage and retrieval
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # sensitive
    treatment_plan: str     # sensitive

# In a real system this would be a database query
_patient_db: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    ),
    "p002": Patient(
        id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, avoid allergens"
    ),
}

def get_patient_by_id(patient_id: str) -> Patient:
    """Retrieve a patient from the mock database."""
    patient = _patient_db.get(patient_id)
    if not patient:
        raise ValueError(f"Patient with id '{patient_id}' not found.")
    return patient

# --------------------------------------------------------------------
# Report generation
# --------------------------------------------------------------------

_ALLOWED_PLACEHOLDERS = {"patient.name", "patient.age"}

_placeholder_pattern = re.compile(r"\{([^{}]+)\}")

def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string by replacing placeholders in the template
    with data from the patient identified by `patient_id`.

    Only `{patient.name}` and `{patient.age}` are allowed placeholders.
    Any other placeholder or missing patient data will raise ValueError.

    Parameters
    ----------
    patient_id : str
        Identifier of the patient.
    template : str
        Template containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient cannot be found, if a placeholder is not allowed,
        or if any other error occurs during formatting.
    """
    try:
        patient = get_patient_by_id(patient_id)
    except Exception as exc:
        raise ValueError(f"Failed to retrieve patient data: {exc}") from exc

    def _replace(match: re.Match) -> str:
        key = match.group(1).strip()
        if key not in _ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Unauthorized placeholder '{key}' detected.")
        # Map allowed placeholders to actual patient attributes
        if key == "patient.name":
            return str(patient.name)
        elif key == "patient.age":
            return str(patient.age)
        # Should never reach here because of the allowed set
        raise ValueError(f"Unhandled placeholder '{key}'.")

    try:
        result = _placeholder_pattern.sub(_replace, template)
    except Exception as exc:
        raise ValueError(f"Error processing template: {exc}") from exc

    return result