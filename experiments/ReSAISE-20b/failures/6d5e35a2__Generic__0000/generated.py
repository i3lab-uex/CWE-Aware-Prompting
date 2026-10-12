import re
from dataclasses import dataclass
from typing import Dict

# ------------------------------------------------------------------
# Mock patient database and Patient class
# ------------------------------------------------------------------
@dataclass
class Patient:
    """Represents a patient record."""
    pat_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# In a real system this would be replaced by a database query.
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        pat_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, 10mg daily"
    ),
    "P002": Patient(
        pat_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ------------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------------
def _get_patient(pat_id: str) -> Patient:
    """
    Retrieve a patient from the database.
    Raises ValueError if the ID is not found.
    """
    patient = PATIENT_DB.get(pat_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {pat_id}")
    return patient

def _extract_placeholders(layout: str) -> set:
    """
    Extract all placeholder names from a format string.
    Placeholders are expected in the form {patient.<field>}.
    """
    # Regex to match {patient.field}
    pattern = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    return set(pattern.findall(layout))

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a patient report by replacing placeholders in the layout
    with actual patient data.

    Parameters:
        pat_id (str): Unique identifier of the patient.
        layout (str): Report template containing placeholders like
                      '{patient.name}' or '{patient.age}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the patient ID is invalid or if restricted
                    information (diagnosis, treatment_plan) is requested.
    """
    # Define fields that are considered restricted
    RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

    # Retrieve patient record
    patient = _get_patient(pat_id)

    # Extract placeholders from layout
    placeholders = _extract_placeholders(layout)

    # Check for restricted fields
    if RESTRICTED_FIELDS & placeholders:
        raise ValueError(
            f"Attempt to access restricted fields: {RESTRICTED_FIELDS & placeholders}"
        )

    # Build a mapping for formatting
    patient_data = {
        "name": patient.name,
        "age": str(patient.age),
        "gender": patient.gender
    }

    # Replace placeholders safely
    try:
        formatted_report = layout.format(patient=patient_data)
    except KeyError as e:
        # Placeholder refers to a non‑existent field
        raise ValueError(f"Unknown placeholder: {e}") from e

    return formatted_report

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     template = (
#         "Patient Report\n"
#         "Name: {patient.name}\n"
#         "Age: {patient.age}\n"
#         "Gender: {patient.gender}\n"
#     )
#     print(create_patient_report("P001", template))