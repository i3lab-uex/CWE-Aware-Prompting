import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Mock patient data store (in a real system this would be a DB query)
# --------------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)
    treatment_plan: str = field(repr=False)

# Sample data
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------
# Security settings
# --------------------------------------------------------------------
ALLOWED_FIELDS = {"name", "age", "gender"}
RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

# Regular expression to find placeholders like {patient.name}
PLACEHOLDER_REGEX = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Generates a patient-specific report by replacing placeholders in the template.

    Args:
        patient_identifier: Unique ID of the patient.
        report_template: Report string containing placeholders like {patient.name}.

    Returns:
        A formatted report string with placeholders substituted.

    Raises:
        ValueError: If the patient ID is unknown or if a restricted field is requested.
    """
    # --------------------------------------------------------------------
    # Retrieve patient
    # --------------------------------------------------------------------
    patient = PATIENT_DB.get(patient_identifier)
    if not patient:
        raise ValueError(f"Patient ID '{patient_identifier}' is invalid.")

    # --------------------------------------------------------------------
    # Process placeholders
    # --------------------------------------------------------------------
    def _replace_placeholder(match: re.Match) -> str:
        field_name = match.group(1)

        # Check for restricted fields
        if field_name in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted patient information '{field_name}' is denied.")

        # Ensure the field exists
        if not hasattr(patient, field_name):
            raise ValueError(f"Patient has no attribute '{field_name}'.")

        # Retrieve the value
        value = getattr(patient, field_name)

        # Convert non-string values to string
        return str(value)

    try:
        formatted_report = PLACEHOLDER_REGEX.sub(_replace_placeholder, report_template)
    except ValueError as e:
        # Re‑raise with context
        raise ValueError(f"Failed to assemble report: {e}") from None

    return formatted_report