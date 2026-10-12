import re
from typing import Dict

# --------------------------------------------------------------------------- #
#   Mocked / placeholder components – in a real system these would be
#   provided by the application framework or database layer.
# --------------------------------------------------------------------------- #

class Patient:
    """Simple data holder for patient information."""
    def __init__(self, patient_id: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan

# Simulated patient store (in a real system this would be a DB query)
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient("P001", "Alice Smith", 29, "Female",
                    "Hypertension", "Lifestyle modification"),
    "P002": Patient("P002", "Bob Johnson", 45, "Male",
                    "Type II Diabetes", "Metformin"),
}

def get_patient_by_id(patient_identifier: str) -> Patient:
    """
    Retrieve a patient instance by ID.
    Raises KeyError if the ID does not exist.
    """
    try:
        return PATIENT_DB[patient_identifier]
    except KeyError as exc:
        raise ValueError(f"Invalid patient identifier: {patient_identifier}") from exc

# --------------------------------------------------------------------------- #
#   Core functionality
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = {"name", "age", "gender"}  # fields that may appear in templates

PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Build a patient‑specific report by substituting placeholders in
    *report_template* with data from the patient record.

    Parameters
    ----------
    patient_identifier : str
        The unique identifier of the patient.
    report_template : str
        Template containing placeholders such as `{patient.name}`.

    Returns
    -------
    str
        The report with all placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient identifier is invalid or if the template tries to
        access a restricted field.
    """
    # Retrieve patient – raises ValueError if not found
    patient = get_patient_by_id(patient_identifier)

    # Find all placeholders in the template
    placeholders = PLACEHOLDER_PATTERN.findall(report_template)

    # Ensure no duplicate checks are wasted
    unique_placeholders = set(placeholders)

    # Validate that each placeholder references an allowed field
    for field in unique_placeholders:
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted field '{field}' is not allowed in the template."
            )

    # Prepare a mapping from placeholder name to value
    substitution_map = {
        field: getattr(patient, field) for field in unique_placeholders
    }

    # Perform the substitution safely; any missing key will raise KeyError,
    # but that should not happen because we validated fields above.
    try:
        report = report_template.format(patient=substitution_map)
    except KeyError as exc:
        # This should not occur; if it does, treat it as a programming error.
        raise ValueError(f"Failed to substitute placeholder: {exc}") from exc

    return report