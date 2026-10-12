import re
from dataclasses import dataclass
from typing import Dict, Any

# ----------------------------------------------------------------------
# Example Patient data model (would normally come from the real system)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# ----------------------------------------------------------------------
# Mock patient database (replace with real data access in production)
# ----------------------------------------------------------------------
_PATIENT_DB: Dict[str, Patient] = {
    "patient-001": Patient(
        id="patient-001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    # Add more patient entries here
}

# ----------------------------------------------------------------------
# Allowed placeholder fields (exposed to reports)
# ----------------------------------------------------------------------
_ALLOWED_FIELDS = {
    "name",
    "age",
    "gender",
}

# ----------------------------------------------------------------------
# Helper: retrieve patient by ID
# ----------------------------------------------------------------------
def _get_patient_by_id(identifier: str) -> Patient:
    """
    Retrieve a patient object from the database.
    Raises ValueError if the ID is not found.
    """
    patient = _PATIENT_DB.get(identifier)
    if patient is None:
        raise ValueError(f"Invalid patient ID: {identifier}")
    return patient

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Build a personalized patient summary by replacing placeholders
    in the provided template with actual patient data.

    Parameters
    ----------
    identifier : str
        The unique patient ID.
    report_template : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if restricted fields are accessed.
    """
    # Retrieve patient data
    patient = _get_patient_by_id(identifier)

    # Find all placeholders in the template
    pattern = re.compile(r"\{patient\.([^\}]+)\}")
    placeholders = set(pattern.findall(report_template))

    # Validate each placeholder
    for field in placeholders:
        if field not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Attempt to access restricted or unknown field '{field}' "
                "in report template."
            )

    # Prepare a mapping for allowed fields
    patient_dict: Dict[str, Any] = {
        field: getattr(patient, field) for field in placeholders
    }

    # Perform safe replacement
    def _replace(match: re.Match) -> str:
        field_name = match.group(1)
        return str(patient_dict[field_name])

    formatted_report = pattern.sub(_replace, report_template)

    return formatted_report

# ----------------------------------------------------------------------
# Example usage (for testing purposes)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    try:
        report = build_patient_summary("patient-001", template)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")