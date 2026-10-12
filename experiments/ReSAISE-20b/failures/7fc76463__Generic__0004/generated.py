import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Mock patient database and access layer
# ------------------------------------------------------------------

@dataclass
class Patient:
    """Represents a patient's basic data."""
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# In a real system this would query a database or an API.
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="Alice Smith",
        age=34,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lisinopril 10mg daily"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Bob Johnson",
        age=58,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Metformin 500mg twice daily"
    ),
}

# ------------------------------------------------------------------
# Security policy: define which fields are allowed to be exposed
# ------------------------------------------------------------------

ALLOWED_FIELDS = {
    "name",
    "age",
    "gender",
    "treatment_plan",  # assume this is non‑sensitive
}

# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------

PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Builds a patient summary by substituting placeholders in the report_template
    with actual patient data.

    Args:
        identifier (str): Unique patient ID.
        report_template (str): Template string containing placeholders like
                               '{patient.name}', '{patient.age}'.

    Returns:
        str: The formatted report with placeholders replaced by patient data.

    Raises:
        ValueError: If the patient ID is not found or if a restricted field
                    (e.g., diagnosis) is requested in the template.
    """
    # 1. Retrieve patient
    patient = PATIENT_DB.get(identifier)
    if not patient:
        raise ValueError(f"Invalid patient identifier: {identifier}")

    # 2. Find all placeholders
    matches = PLACEHOLDER_PATTERN.findall(report_template)
    if not matches:
        # No placeholders – return the template unchanged
        return report_template

    # 3. Resolve each placeholder safely
    resolved_values = {}
    for field_name in set(matches):
        if field_name not in ALLOWED_FIELDS:
            raise ValueError(f"Access to restricted field '{field_name}' is not allowed.")
        # Use getattr on the patient dataclass
        resolved_values[field_name] = str(getattr(patient, field_name))

    # 4. Perform substitution
    def replacer(match: re.Match) -> str:
        field = match.group(1)
        return resolved_values.get(field, match.group(0))

    formatted_report = PLACEHOLDER_PATTERN.sub(replacer, report_template)
    return formatted_report

# ------------------------------------------------------------------
# Example usage (for testing only – remove or comment out in production)
# ------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )
    print(build_patient_summary("P001", template))