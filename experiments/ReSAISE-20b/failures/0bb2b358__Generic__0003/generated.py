import re
from dataclasses import dataclass, asdict

# --------------------------------------------------------------------------- #
# Mock patient database (in a real system this would be replaced by a DB call)
# --------------------------------------------------------------------------- #
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# Example patients – replace with actual data source in production
PATIENT_DB = {
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
        age=32,
        gender="Female",
        diagnosis="Diabetes Type II",
        treatment_plan="Insulin therapy, Diet plan"
    ),
}

# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #
def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient object from the database.
    Raises ValueError if the patient does not exist.
    """
    patient = PATIENT_DB.get(patient_id)
    if patient is None:
        raise ValueError(f"Patient with ID '{patient_id}' not found.")
    return patient

def _sanitize_template(template: str, allowed_fields: set) -> None:
    """
    Validate that all placeholders in the template are within the allowed set.
    Raises ValueError if an invalid placeholder is detected.
    """
    # Find all placeholders of the form {patient.<field>}
    pattern = r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    for match in re.finditer(pattern, template):
        field = match.group(1)
        if field not in allowed_fields:
            raise ValueError(f"Unauthorized placeholder '{{patient.{field}}}' detected.")

def _safe_format(template: str, data: dict) -> str:
    """
    Perform a safe formatting operation that only replaces known placeholders.
    Raises ValueError if any placeholder is missing in data.
    """
    try:
        return template.format(**data)
    except KeyError as e:
        raise ValueError(f"Missing placeholder data for field: {e}") from None
    except Exception as e:
        raise ValueError(f"Error during template formatting: {e}") from None

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string for the given patient based on the provided template.

    Parameters
    ----------
    patient_id : str
        The unique identifier of the patient.
    template : str
        Report template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient is not found, if the template contains unauthorized placeholders,
        or if formatting fails.
    """
    # Retrieve patient data
    patient = _get_patient(patient_id)

    # Convert patient dataclass to a dictionary for formatting
    patient_dict = asdict(patient)

    # Define allowed fields (exclude sensitive data)
    allowed_fields = {
        "patient_id",
        "name",
        "age",
        "gender",
        "diagnosis",
        "treatment_plan",
    }

    # Validate template placeholders
    _sanitize_template(template, allowed_fields)

    # Perform safe formatting
    report = _safe_format(template, patient_dict)
    return report

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = (
        "Patient Report:\n"
        "ID: {patient.patient_id}\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )
    try:
        print(generate_user_report("P001", tmpl))
    except ValueError as err:
        print(f"Error: {err}")