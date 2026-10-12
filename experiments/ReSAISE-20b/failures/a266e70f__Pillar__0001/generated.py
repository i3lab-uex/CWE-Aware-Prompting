import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Data model and in‑memory store                                            #
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False, default="")          # sensitive data
    treatment_plan: str = field(repr=False, default="")     # sensitive data

# In‑memory "database" of patients (for demo purposes)
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
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #

_ALLOWED_FIELDS = {"name", "age", "gender"}

_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return set(match.group(1) for match in _PLACEHOLDER_RE.finditer(template))

def _replace_placeholders(template: str, patient: Patient) -> str:
    """
    Replace placeholders in the template with actual patient data.
    Only allowed fields are substituted; others raise ValueError.
    """
    def _replace(match):
        field_name = match.group(1)
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(f"Access to restricted patient attribute: {field_name}")
        return str(getattr(patient, field_name))
    return _PLACEHOLDER_RE.sub(_replace, template)

# --------------------------------------------------------------------------- #
# Public API                                                                   #
# --------------------------------------------------------------------------- #

def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient report by filling in the provided template with data
    from the patient identified by `id`.

    Parameters:
        id (str): Unique identifier of the patient.
        report_template (str): Template string containing placeholders
                               like '{patient.name}'.

    Returns:
        str: The fully populated report string.

    Raises:
        ValueError: If the patient ID does not exist or if the template
                    attempts to access restricted data.
    """
    # Fetch patient record (resource acquisition)
    patient = PATIENT_DB.get(id)
    if not patient:
        raise ValueError(f"Patient ID '{id}' is invalid or does not exist.")

    # Validate placeholders early (resource release is implicit here)
    placeholders = _extract_placeholders(report_template)
    if not placeholders.issubset(_ALLOWED_FIELDS):
        restricted = placeholders - _ALLOWED_FIELDS
        raise ValueError(f"Template contains restricted fields: {', '.join(restricted)}")

    # Perform substitution
    try:
        report = _replace_placeholders(report_template, patient)
    except ValueError as e:
        # Re‑raise with context
        raise ValueError(f"Error generating report: {e}") from None

    return report

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)                                           #
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("p001", template))