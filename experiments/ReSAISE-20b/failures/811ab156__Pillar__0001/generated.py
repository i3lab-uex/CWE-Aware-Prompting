import re
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Mock Patient data model and repository (simulates secure resource handling)
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# Simulated in‑memory patient database (would be a secure DB in production)
_PATIENT_DB: Dict[str, Patient] = {
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
        diagnosis="Diabetes Type II",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------------- #
# Context manager to ensure the patient record is accessed in a controlled
# manner (CWE‑664 mitigation)
# --------------------------------------------------------------------------- #

@contextmanager
def patient_record(patient_id: str) -> Patient:
    """
    Context manager that yields a Patient object for the given patient_id.
    Raises ValueError if the patient does not exist. The context manager
    ensures that any future cleanup (e.g., closing DB connections) would be
    performed automatically.
    """
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")
    try:
        yield patient
    finally:
        # In a real implementation, resources such as DB cursors would be closed here.
        pass

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _extract_placeholders(template: str) -> set:
    """
    Extracts all placeholders of the form {patient.<field>} from the template.
    """
    return set(re.findall(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}", template))

def _sanitize_and_prepare_mapping(patient: Patient, placeholders: set) -> Dict[str, Any]:
    """
    Builds a mapping dictionary for allowed patient fields.
    Restricted fields (diagnosis, treatment_plan) are omitted unless explicitly
    permitted. For this example, they are considered restricted.
    """
    allowed_fields = {
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
    }
    # If any restricted field is requested, raise an error
    restricted = {"diagnosis", "treatment_plan"}
    if placeholders & restricted:
        raise ValueError(f"Access to restricted patient information: {placeholders & restricted}")
    # Ensure only placeholders that exist in allowed_fields are used
    missing = placeholders - set(allowed_fields.keys())
    if missing:
        raise ValueError(f"Unknown placeholder(s): {missing}")
    return allowed_fields

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Generates a personalized patient report by replacing placeholders in the
    provided template with actual patient data.

    Parameters:
        patient_identifier (str): The unique identifier of the patient.
        report_template (str): A template string containing placeholders such
                               as '{patient.name}'.

    Returns:
        str: The fully formatted report string.

    Raises:
        ValueError: If the patient ID is invalid, if restricted data is requested,
                    or if placeholders reference unknown fields.
    """
    # Validate template format (basic check)
    if not isinstance(report_template, str):
        raise ValueError("report_template must be a string")

    # Extract placeholders
    placeholders = _extract_placeholders(report_template)

    with patient_record(patient_identifier) as patient:
        mapping = _sanitize_and_prepare_mapping(patient, placeholders)
        # Perform safe string formatting
        try:
            formatted_report = report_template.format(patient=mapping)
        except KeyError as e:
            raise ValueError(f"Missing placeholder value: {e}") from e
    return formatted_report

# --------------------------------------------------------------------------- #
# Example usage (commented out; remove comments to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "---------------\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(assemble_patient_report("P001", template))