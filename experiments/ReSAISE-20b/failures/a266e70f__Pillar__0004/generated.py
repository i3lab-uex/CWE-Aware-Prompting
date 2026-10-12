import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Data model and mock storage
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # restricted field
    treatment_plan: str     # restricted field

# In a real system this would be replaced with database access.
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        id="P002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Diabetes Type 2",
        treatment_plan="Insulin therapy"
    ),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
_RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

def _validate_template(template: str):
    """
    Ensure that the template only contains allowed placeholders.
    Placeholders must be of the form {patient.<field>}.
    """
    # Find all placeholders in the template
    pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    for match in pattern.finditer(template):
        field = match.group(1)
        if field in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field}' is not allowed.")
    # Ensure no other braces remain
    if re.search(r"\{[^}]*\}", template):
        raise ValueError("Template contains unsupported placeholder syntax.")

def _get_patient(id: str) -> Patient:
    """
    Retrieve a patient from the mock database.
    Raises ValueError if the ID is not found.
    """
    patient = _PATIENT_DB.get(id)
    if not patient:
        raise ValueError(f"Patient with ID '{id}' does not exist.")
    return patient

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_patient_report(id: str, report_template: str) -> str:
    """
    Generates a patient report by replacing placeholders in the template
    with actual patient data.

    Parameters:
        id (str): The unique identifier of the patient.
        report_template (str): The template string containing placeholders.

    Returns:
        str: The formatted patient report.

    Raises:
        ValueError: If the patient ID is invalid or if the template
                    attempts to access restricted medical data.
    """
    # Validate input and template syntax
    if not isinstance(id, str) or not id:
        raise ValueError("Patient ID must be a non-empty string.")
    if not isinstance(report_template, str):
        raise ValueError("Report template must be a string.")

    _validate_template(report_template)

    # Retrieve patient data
    patient = _get_patient(id)
    patient_dict = asdict(patient)

    # Prepare a safe mapping for formatting
    safe_mapping = {"patient": patient_dict}

    try:
        report = report_template.format(**safe_mapping)
    except KeyError as exc:
        # This should not happen if _validate_template passed
        raise ValueError(f"Unknown placeholder: {exc}") from None

    return report

# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Patient Report:\n"
#         "Name: {patient.name}\n"
#         "Age: {patient.age}\n"
#         "Gender: {patient.gender}\n"
#     )
#     print(create_patient_report("P001", template))