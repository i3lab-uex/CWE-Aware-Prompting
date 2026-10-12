import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Patient data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Immutable patient record."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# ----------------------------------------------------------------------
# In‑memory patient store (simulating a database)
# ----------------------------------------------------------------------
_patient_store: Dict[str, Patient] = {
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
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy",
    ),
}

# ----------------------------------------------------------------------
# Allowed fields for templating (public data only)
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan",
}

# ----------------------------------------------------------------------
# Helper to fetch patient
# ----------------------------------------------------------------------
def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient by ID.

    Raises ValueError if the ID is unknown.
    """
    patient = _patient_store.get(patient_id)
    if not patient:
        raise ValueError(f"Patient ID '{patient_id}' is invalid.")
    return patient

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient report by replacing placeholders in the template.

    Parameters
    ----------
    id : str
        Unique patient identifier.
    report_template : str
        Template string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The filled report string.

    Raises
    ------
    ValueError
        If the patient ID is unknown or a placeholder references a restricted field.
    """
    # Retrieve patient record
    patient = _get_patient(id)

    # Convert the patient to a dict for easy lookup
    patient_dict = asdict(patient)
    patient_data = patient_dict.copy()
    # Remove the 'id' field from templating scope
    patient_data.pop("id", None)

    # Find all placeholders of the form {patient.field}
    pattern = r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    placeholders = re.findall(pattern, report_template)

    # Validate each placeholder
    for field in set(placeholders):
        if field not in _ALLOWED_FIELDS:
            raise ValueError(f"Access to restricted or unknown patient data: '{field}'")
        if field not in patient_data:
            raise ValueError(f"Patient data missing required field: '{field}'")

    # Prepare the formatting dictionary
    format_dict = {"patient": patient_data}

    try:
        report = report_template.format(**format_dict)
    except KeyError as exc:
        # This should not happen due to validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report