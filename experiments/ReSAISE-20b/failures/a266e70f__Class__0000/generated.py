import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Mock patient data store (in a real system this would be a database)
# ------------------------------------------------------------------
@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str  # Sensitive data
    treatment_plan: str  # Sensitive data

# Sample patients (for illustration only)
PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "p002": Patient(
        id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes Type II",
        treatment_plan="Insulin therapy"
    ),
}

# ------------------------------------------------------------------
# Allowed placeholders (only non-sensitive fields)
# ------------------------------------------------------------------
ALLOWED_PLACEHOLDERS = {"patient.name", "patient.age", "patient.gender"}

# ------------------------------------------------------------------
# Utility: Extract placeholders from template
# ------------------------------------------------------------------
PLACEHOLDER_REGEX = re.compile(r"\{([^{}]+)\}")

def _extract_placeholders(template: str):
    """Return a set of unique placeholders found in the template."""
    return {match.group(1) for match in PLACEHOLDER_REGEX.finditer(template)}

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient report by replacing placeholders in the template
    with actual patient data.

    Parameters:
        id (str): Unique patient identifier.
        report_template (str): Template containing placeholders.

    Returns:
        str: Report with placeholders replaced by patient data.

    Raises:
        ValueError: If the patient ID is invalid or if a restricted
                    placeholder is used.
    """
    # Validate patient exists
    patient = PATIENT_DB.get(id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {id}")

    # Extract placeholders and validate them
    placeholders = _extract_placeholders(report_template)
    for ph in placeholders:
        if ph not in ALLOWED_PLACEHOLDERS:
            raise ValueError(
                f"Access to restricted data or unknown placeholder: {ph}"
            )

    # Build a mapping for allowed placeholders
    context = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender,
    }

    # Perform replacement
    def _replace(match):
        key = match.group(1)
        return context.get(key, f"{{{key}}}")  # Should never miss

    report = PLACEHOLDER_REGEX.sub(_replace, report_template)
    return report