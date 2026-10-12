import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------
# Patient data model (simplified)
# ----------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str
    # Sensitive fields that must not be exposed via templates
    ssn: str = None
    insurance_number: str = None


# ----------------------------------------------------
# In‑memory patient store (replace with real DB in production)
# ----------------------------------------------------
_PATIENT_STORE: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication and lifestyle changes",
        ssn="123-45-6789",
        insurance_number="INS-987654"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes Type II",
        treatment_plan="Insulin therapy and diet management",
    ),
}


# ----------------------------------------------------
# Helper utilities
# ----------------------------------------------------
_ALLOWED_FIELDS = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan"
}

_PLACEHOLDER_PATTERN = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")


def _validate_template(template: str) -> None:
    """
    Ensure that the template only contains allowed placeholders.
    Raise ValueError if an unsupported placeholder is found.
    """
    for match in _PLACEHOLDER_PATTERN.finditer(template):
        field_name = match.group(1)
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(f"Disallowed placeholder: '{{patient.{field_name}}}'")


def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient by ID from the store.
    Raise ValueError if not found.
    """
    patient = _PATIENT_STORE.get(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID '{patient_id}' not found")
    return patient


# ----------------------------------------------------
# Main function
# ----------------------------------------------------
def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report for the given patient based on the provided template.

    Args:
        patient_id: The unique identifier of the patient.
        template: A string containing placeholders like '{patient.name}'.

    Returns:
        The formatted report string.

    Raises:
        ValueError: If the patient is not found, if the template contains
                    disallowed placeholders, or if any other error occurs.
    """
    try:
        # Validate template placeholders
        _validate_template(template)

        # Retrieve patient data
        patient = _get_patient(patient_id)
        patient_dict = {f"patient.{k}": v for k, v in asdict(patient).items()
                        if k in _ALLOWED_FIELDS}

        # Perform formatting
        report = template.format_map(patient_dict)
        return report

    except KeyError as exc:
        raise ValueError(f"Missing placeholder data: {exc}") from exc
    except Exception as exc:
        # Catch-all for unforeseen errors; do not expose internal details
        raise ValueError("An error occurred while generating the report") from exc


# ----------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )
    print(generate_user_report("P001", tmpl))