import re
from dataclasses import dataclass, asdict
from typing import Dict

# ------------------------------------------------------------------
# Data model and in‑memory store
# ------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive data – not exposed in reports
    treatment_plan: str     # Sensitive data – not exposed in reports


# Example patient database (replace with real persistence layer)
_patient_db: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, 5mg daily"
    ),
    "p002": Patient(
        id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, 2 puffs twice daily"
    ),
}


# ------------------------------------------------------------------
# Helper utilities
# ------------------------------------------------------------------

def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient from the database.
    Raises ValueError if the ID is unknown.
    """
    try:
        return _patient_db[patient_id]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{patient_id}' is invalid.") from exc


def _extract_placeholders(template: str) -> set[str]:
    """
    Extract placeholders from a format string.
    Supports the syntax {patient.<field>}.
    """
    pattern = r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}"
    return set(re.findall(pattern, template))


# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------

def create_patient_report(id: str, report_template: str) -> str:
    """
    Create a patient report by replacing placeholders in the template
    with actual data from the specified patient.

    Parameters:
        id (str): Unique patient identifier.
        report_template (str): Template containing placeholders
            like '{patient.name}' or '{patient.age}'.

    Returns:
        str: The formatted report string.

    Raises:
        ValueError: If the patient ID is unknown or if the template
                    attempts to access restricted medical data.
    """
    # Retrieve patient record
    patient = _get_patient(id)

    # Allowed fields for public reporting
    allowed_fields = {"name", "age", "gender"}

    # Extract placeholders and validate them
    placeholders = _extract_placeholders(report_template)
    for field in placeholders:
        if field not in allowed_fields:
            raise ValueError(
                f"Access to restricted patient data '{field}' is not allowed."
            )

    # Build a mapping for format() – use nested dict to match the template syntax
    patient_dict = asdict(patient)
    safe_data = {k: v for k, v in patient_dict.items() if k in allowed_fields}
    context = {"patient": safe_data}

    # Perform the formatting
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # This can happen if the template contains a placeholder
        # that was not extracted by _extract_placeholders (e.g., typo)
        raise ValueError(f"Invalid placeholder in template: {exc}") from exc

    return report


# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("p001", template))