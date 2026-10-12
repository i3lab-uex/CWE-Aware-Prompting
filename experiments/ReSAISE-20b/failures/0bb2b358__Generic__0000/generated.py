import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Patient data model (simplified for this example)
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """Represents a patient in the healthcare system."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# --------------------------------------------------------------------------- #
# In‑memory patient store (replace with real database access in production)
# --------------------------------------------------------------------------- #

_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication",
    ),
    "p002": Patient(
        id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy and diet modification",
    ),
}

def get_patient_by_id(patient_id: str) -> Patient:
    """
    Retrieve a patient object by ID.
    Raises KeyError if the patient does not exist.
    """
    try:
        return _PATIENT_DB[patient_id]
    except KeyError as exc:
        raise ValueError(f"Patient with ID '{patient_id}' not found.") from exc

# --------------------------------------------------------------------------- #
# Report generation logic
# --------------------------------------------------------------------------- #

# Allowed attributes that can appear in the template.
_ALLOWED_ATTRIBUTES = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan",
}

# Regex to find placeholders of the form {patient.attribute}
_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string for the specified patient by filling in
    placeholders from the provided template.

    Parameters
    ----------
    patient_id : str
        The unique identifier of the patient.
    template : str
        A string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The rendered report string with placeholders replaced by actual data.

    Raises
    ------
    ValueError
        If the patient does not exist, if a placeholder references an
        unauthorized attribute, or if any other error occurs during rendering.
    """
    # Fetch patient data
    try:
        patient = get_patient_by_id(patient_id)
    except Exception as exc:
        raise ValueError(f"Failed to retrieve patient data: {exc}") from exc

    # Find all placeholders in the template
    placeholders = _PLACEHOLDER_RE.findall(template)

    # Validate that all referenced attributes are allowed
    for attr in placeholders:
        if attr not in _ALLOW_ATTRIBS = _ALLOWED_ATTRIBUTES:
            raise ValueError(f"Unauthorized attribute '{attr}' in template.")

    # Build a mapping for placeholder replacement
    context: Dict[str, Any] = {attr: getattr(patient, attr) for attr in placeholders}

    # Perform safe replacement
    try:
        rendered = template.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Failed to render template: {exc}") from exc

    return rendered

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     tmpl = (
#         "Patient Report\n"
#         "Name: {patient.name}\n"
#         "Age: {patient.age}\n"
#         "Diagnosis: {patient.diagnosis}\n"
#         "Treatment Plan: {patient.treatment_plan}"
#     )
#     print(generate_user_report("p001", tmpl))