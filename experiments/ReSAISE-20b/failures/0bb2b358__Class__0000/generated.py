import re
from dataclasses import dataclass

# Example Patient class; in real code this would be imported from the system
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# Simulated patient database (replace with real persistence layer)
_PATIENT_DB = {
    "123": Patient(
        patient_id="123",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    ),
    "456": Patient(
        patient_id="456",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# Allowed placeholders to prevent accidental exposure of sensitive data
_ALLOWED_FIELDS = {
    "patient.name",
    "patient.age",
    "patient.gender",
    "patient.diagnosis",
    "patient.treatment_plan",
}

_PLACEHOLDER_RE = re.compile(r"\{([^}]+)\}")

def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string by replacing placeholders in the template with
    corresponding patient attributes.

    Args:
        patient_id: The ID of the patient.
        template: A string containing placeholders such as '{patient.name}'.

    Returns:
        The report string with all placeholders substituted.

    Raises:
        ValueError: If the patient ID is not found, if a placeholder
                    references an unsupported field, or if any other error
                    occurs during processing.
    """
    # Retrieve patient from the simulated database
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID '{patient_id}' not found.")

    # Prepare a mapping of allowed placeholders to their values
    placeholder_map = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender,
        "patient.diagnosis": patient.diagnosis,
        "patient.treatment_plan": patient.treatment_plan,
    }

    # Function to replace each placeholder
    def _replace(match):
        key = match.group(1).strip()
        if key not in _ALLOWED_FIELDS:
            raise ValueError(f"Unauthorized placeholder '{key}'.")
        return placeholder_map[key]

    try:
        result = _PLACEHOLDER_RE.sub(_replace, template)
    except Exception as e:
        # Any unexpected error is treated as a potential security issue
        raise ValueError(f"Error generating report: {e}") from e

    return result