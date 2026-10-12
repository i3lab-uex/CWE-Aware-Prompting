import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Simulated patient storage and model
# ----------------------------------------------------------------------
class Patient:
    """
    Simple data holder for patient information.
    In a real system this would interface with a database or
    an external service.  Only attributes that are safe to expose
    through the report template should be defined here.
    """
    __slots__ = ("patient_id", "name", "age", "gender",
                 "diagnosis", "treatment_plan")

    def __init__(self, patient_id: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis
        self.treatment_plan = treatment_plan


# Example in‑memory datastore; replace with real persistence layer.
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication."
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy and diet."
    ),
}


# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient object from the datastore.
    Raises ValueError if the patient does not exist.
    """
    try:
        return PATIENT_DB[patient_id]
    except KeyError as exc:
        raise ValueError(f"Patient with ID '{patient_id}' not found") from exc


def _extract_placeholders(template: str) -> set:
    """
    Extract placeholder names from the template string.
    Only simple attribute access like {patient.name} is supported.
    """
    # Regex for `{object.attribute}` where object and attribute are word chars
    pattern = r"\{(?P<object>\w+)\.(?P<attr>\w+)\}"
    return {f"{m.group('object')}.{m.group('attr')}" for m in re.finditer(pattern, template)}


# ----------------------------------------------------------------------
# Core functionality
# ----------------------------------------------------------------------
def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string for the specified patient using the given template.
    
    The template may contain placeholders in the form `{patient.<attribute>}`.
    Only a predefined set of attributes are allowed to be accessed.  Any attempt
    to access an unauthorized attribute will raise a ValueError.

    Args:
        patient_id: The unique identifier of the patient.
        template:   A string containing placeholders.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the patient does not exist, if a placeholder references
                    an unauthorized attribute, or if formatting fails.
    """
    # Retrieve patient data
    patient = _get_patient(patient_id)

    # Define allowed placeholders
    ALLOWED_PLACEHOLDERS = {
        "patient.name",
        "patient.age",
        "patient.gender",
        "patient.diagnosis",
        "patient.treatment_plan",
    }

    # Validate placeholders
    found_placeholders = _extract_placeholders(template)
    unauthorized = found_placeholders - ALLOWED_PLACEHOLDERS
    if unauthorized:
        raise ValueError(f"Unauthorized placeholder(s) detected: {', '.join(sorted(unauthorized))}")

    # Build mapping for formatting
    mapping = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender,
        "patient.diagnosis": patient.diagnosis,
        "patient.treatment_plan": patient.treatment_plan,
    }

    try:
        report = template.format(**mapping)
    except Exception as exc:
        # Any formatting error is considered a security risk
        raise ValueError(f"Failed to format report: {exc}") from exc

    return report