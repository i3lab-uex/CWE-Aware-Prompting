import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Simulated patient data store and Patient model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Represents a patient record in the system."""
    pat_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str


# Example in‑memory data store (in a real system this would be a DB call)
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        pat_id="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        pat_id="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Medication B, Diet plan"
    ),
}


# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_patient(pat_id: str) -> Patient:
    """Retrieve a patient record by ID or raise ValueError."""
    patient = _PATIENT_DB.get(pat_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {pat_id}")
    return patient


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a patient report by substituting placeholders in the provided
    layout string with data from the corresponding Patient record.

    Parameters:
        pat_id (str): Unique identifier of the patient.
        layout (str): Report template containing placeholders such as
                      '{patient.name}', '{patient.age}', etc.

    Returns:
        str: The fully formatted report string.

    Raises:
        ValueError: If the patient ID is not found or if a restricted
                    field (e.g., diagnosis, treatment_plan) is accessed.
    """
    # Allowed fields for substitution
    ALLOWED_FIELDS = {"name", "age", "gender"}

    # Fetch patient record
    patient = _get_patient(pat_id)

    # Regular expression to capture placeholders like {patient.name}
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def _replacement(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(
                f"Access to restricted patient information '{field_name}' is not allowed."
            )
        # Retrieve the attribute value safely
        value = getattr(patient, field_name)
        return str(value)

    # Perform the substitution
    try:
        formatted_report = placeholder_pattern.sub(_replacement, layout)
    except ValueError as exc:
        # Re‑raise to propagate error
        raise

    return formatted_report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "---------------\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("P001", template))