import re
from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------
# Dummy patient database and access control (for illustration purposes)
# --------------------------------------------------------------------

@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive data
    treatment_plan: str     # Sensitive data

# In‑memory patient store (in a real system this would be a DB query)
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
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, Regular check‑ups"
    ),
}

# Attributes that are considered public and can be exposed in reports
_PUBLIC_ATTRIBUTES = {"name", "age", "gender"}

# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by replacing placeholders in the template
    with public attributes of the specified patient.

    Parameters:
        patient_id (str): Unique identifier for a patient.
        report_template (str): Template containing placeholders like
                               '{patient.name}'.

    Returns:
        str: The filled report string.

    Raises:
        ValueError: If the patient_id is unknown or if the template
                    attempts to access restricted attributes.
    """
    # ------------------------------------------------------------------
    # 1. Validate patient existence
    # ------------------------------------------------------------------
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Patient ID '{patient_id}' is invalid or does not exist.")

    # ------------------------------------------------------------------
    # 2. Parse placeholders and validate accessed attributes
    # ------------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(report_template)

    for attr in set(placeholders):
        if attr not in _PUBLIC_ATTRIBUTES:
            raise ValueError(
                f"Access to restricted patient attribute '{attr}' is not allowed."
            )

    # ------------------------------------------------------------------
    # 3. Prepare a safe mapping for formatting
    # ------------------------------------------------------------------
    patient_data: Dict[str, Any] = {attr: getattr(patient, attr) for attr in _PUBLIC_ATTRIBUTES}

    # ------------------------------------------------------------------
    # 4. Perform safe formatting
    # ------------------------------------------------------------------
    try:
        filled_report = report_template.format(patient=patient_data)
    except KeyError as e:
        # Should not happen because we validated attributes, but guard anyway
        raise ValueError(f"Missing patient attribute in template: {e}") from e

    return filled_report


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Summary:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}"
    )
    print(generate_patient_summary("P001", template))