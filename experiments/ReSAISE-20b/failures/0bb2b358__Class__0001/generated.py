import re
from typing import Any, Dict

# Mocked database of patients for demonstration purposes.
# In a real system this would interface with a secure data store.
_PATIENT_DB: Dict[str, "Patient"] = {}

class Patient:
    """Simple patient data holder."""
    def __init__(self, patient_id: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan

    def __repr__(self):
        return f"<Patient {self.patient_id}: {self.name}>"

# Whitelist of attributes that are allowed to be exposed via the template.
_ALLOWED_PATIENT_FIELDS = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan"
}

# Regular expression to find placeholders in the template.
_PLACEHOLDER_RE = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _get_patient_by_id(patient_id: str) -> Patient:
    """
    Retrieve a patient object from the database.
    Raises ValueError if not found or access is denied.
    """
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID '{patient_id}' does not exist.")
    return patient

def _safe_format(template: str, context: Dict[str, Any]) -> str:
    """
    Safely format the template using only allowed placeholders.
    Raises ValueError if an unauthorized placeholder is detected.
    """
    def replace_match(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in _ALLOWED_PATIENT_FIELDS:
            raise ValueError(f"Unauthorized placeholder '{{patient.{field_name}}}' detected.")
        value = context.get(field_name)
        # Convert non-string values to string safely.
        return str(value) if value is not None else ""

    # Perform replacement
    return _PLACEHOLDER_RE.sub(replace_match, template)

def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a patient report based on the provided template.

    Parameters
    ----------
    patient_id : str
        The unique identifier of the patient.
    template : str
        Report template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The rendered report string with placeholders substituted by actual data.

    Raises
    ------
    ValueError
        If the patient does not exist, if a placeholder is unauthorized,
        or if any other error occurs during report generation.
    """
    try:
        patient = _get_patient_by_id(patient_id)
        # Build context with only whitelisted fields.
        context = {field: getattr(patient, field) for field in _ALLOWED_PATIENT_FIELDS}
        report = _safe_format(template, context)
        return report
    except Exception as exc:
        # Log the error in a real system; here we simply re-raise with a generic message.
        raise ValueError(f"Failed to generate report: {exc}") from exc

# Example usage (this part would normally be in a separate test module):
if __name__ == "__main__":
    # Populate mock database
    _PATIENT_DB["123"] = Patient(
        patient_id="123",
        name="Jane Doe",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication and lifestyle changes"
    )

    template_str = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )

    print(generate_user_report("123", template_str))