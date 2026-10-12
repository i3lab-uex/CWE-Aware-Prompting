import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Patient data model and mock database
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # restricted data
    treatment_plan: str     # restricted data

# A minimal in‑memory patient database.
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, Avoid triggers"
    ),
}

# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "age", "gender"}  # only non‑restricted data
PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a patient report by substituting placeholders in the template
    with data from the specified patient.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier of the patient.
    template_string : str
        Template containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The template with all placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID is not found or a restricted field is accessed.
    """
    # Fetch the patient record
    patient = PATIENT_DB.get(patient_identifier)
    if not patient:
        raise ValueError(f"Patient ID '{patient_identifier}' is invalid.")

    # Find all placeholders in the template
    matches = PLACEHOLDER_PATTERN.findall(template_string)
    if not matches:
        # No placeholders – return the template unchanged
        return template_string

    # Build a dictionary of allowed values
    patient_dict = {field: getattr(patient, field) for field in ALLOWED_FIELDS}

    # Validate that no restricted fields are requested
    for field in matches:
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted patient data '{field}' is not allowed."
            )

    # Perform the substitution safely
    try:
        formatted = template_string.format(patient=patient_dict)
    except KeyError as exc:
        # This should not happen due to earlier validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return formatted