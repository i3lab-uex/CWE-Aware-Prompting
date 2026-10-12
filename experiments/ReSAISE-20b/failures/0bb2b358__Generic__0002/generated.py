import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Patient model and storage (in a real system this would come from a DB)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str
    # Sensitive fields that must never be exposed via the report
    ssn: str = field(repr=False, default="")
    medical_record_number: str = field(repr=False, default="")

# Example patient registry (in practice this would be replaced with a DB lookup)
PATIENT_REGISTRY: Dict[str, Patient] = {
    "12345": Patient(
        patient_id="12345",
        name="John Doe",
        age=42,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, ACE inhibitors",
        ssn="123-45-6789",
        medical_record_number="MRN001"
    ),
    # Add more patients as needed
}

# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------
ALLOWED_PATIENT_ATTRIBUTES = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan",
}

PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report for the given patient by replacing placeholders in
    `template` with actual patient data.

    Args:
        patient_id: The ID of the patient.
        template: A string containing placeholders like `{patient.name}`.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the patient does not exist, a placeholder references
                    an unknown or disallowed attribute, or any other error occurs.
    """
    try:
        patient = PATIENT_REGISTRY.get(patient_id)
        if not patient:
            raise ValueError(f"Patient with ID '{patient_id}' not found.")

        def replace_placeholder(match: re.Match) -> str:
            attr_name = match.group(1)
            if attr_name not in ALLOWED_PATIENT_ATTRIBUTES:
                raise ValueError(
                    f"Access to patient attribute '{attr_name}' is not allowed."
                )
            value = getattr(patient, attr_name)
            return str(value)

        report = PLACEHOLDER_PATTERN.sub(replace_placeholder, template)
        return report

    except Exception as exc:
        # Wrap any exception into ValueError for consistency
        raise ValueError(f"Failed to generate report: {exc}") from exc

# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )
    try:
        print(generate_user_report("12345", tmpl))
    except ValueError as e:
        print(e)