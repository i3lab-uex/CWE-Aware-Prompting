import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------------------------
# Mock patient data store (in a real system this would be a database)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Restricted field
    treatment_plan: str     # Restricted field

# Example patients (for demonstration purposes)
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy"
    ),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_patient(patient_id: str) -> Patient:
    """Retrieve a patient by ID from the mock database."""
    try:
        return _PATIENT_DB[patient_id]
    except KeyError:
        raise ValueError(f"Invalid patient ID: {patient_id}") from None

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    # Matches {patient.<attribute>} or {{...}} for escaped braces
    pattern = r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}"
    return set(re.findall(pattern, template))

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by filling placeholders in the given template
    with data from the specified patient.

    Parameters:
        patient_id (str): The unique identifier of the patient.
        report_template (str): Template string containing placeholders
                               like '{patient.name}', '{patient.age}'.

    Returns:
        str: The formatted summary string.

    Raises:
        ValueError: If the patient ID is invalid or if the template
                    attempts to access restricted data.
    """
    # Allowed public attributes
    PUBLIC_FIELDS = {"name", "age", "gender"}

    patient = _get_patient(patient_id)

    # Find all placeholders in the template
    placeholders = _extract_placeholders(report_template)

    # Validate that only public fields are used
    restricted_used = placeholders - PUBLIC_FIELDS
    if restricted_used:
        raise ValueError(
            f"Attempt to access restricted data fields: {', '.join(sorted(restricted_used))}"
        )

    # Prepare a mapping for format()
    patient_dict = asdict(patient)
    # Only include public fields
    format_map = {f"patient.{key}": patient_dict[key] for key in PUBLIC_FIELDS}

    # Replace placeholders using str.format_map to avoid KeyError
    try:
        result = report_template.format(**format_map)
    except KeyError as exc:
        # This should not happen because we validated fields, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from None

    return result