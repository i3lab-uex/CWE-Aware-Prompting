import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Data model and sample data store (would normally come from a DB)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive field
    treatment_plan: str     # Sensitive field

# Sample in‑memory patient repository.
_PATIENT_DB: Dict[str, Patient] = {
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
        diagnosis="Asthma",
        treatment_plan="Inhaler B"
    ),
}

# ----------------------------------------------------------------------
# Utility: safe placeholder resolution
# ----------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"\{([^\{\}]+)\}")

def _resolve_placeholders(template: str, patient: Patient) -> str:
    """
    Replace placeholders in the template with patient attributes.
    Only a whitelist of safe fields is allowed. Any attempt to
    reference a restricted field raises ValueError.
    """
    # Define which patient attributes are safe to expose
    SAFE_FIELDS = {
        "patient.name",
        "patient.age",
        "patient.gender",
    }

    def repl(match: re.Match) -> str:
        key = match.group(1).strip()
        if key not in SAFE_FIELDS:
            raise ValueError(f"Access to restricted field '{key}' is denied.")
        # Map placeholder key to Patient attribute
        attr_name = key.split(".", 1)[-1]
        return str(getattr(patient, attr_name))

    # Perform substitution
    return _PLACEHOLDER_RE.sub(repl, template)

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Generate a patient‑specific report from a template.

    Parameters
    ----------
    identifier : str
        Unique patient ID.
    report_template : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is not found or if a restricted field is referenced.
    """
    # Validate identifier
    patient = _PATIENT_DB.get(identifier)
    if not patient:
        raise ValueError(f"Patient ID '{identifier}' is invalid or does not exist.")

    # Resolve placeholders safely
    try:
        formatted_report = _resolve_placeholders(report_template, patient)
    except ValueError as exc:
        # Re‑raise with context
        raise ValueError(f"Failed to build report: {exc}") from None

    return formatted_report

# ----------------------------------------------------------------------
# Example usage (would normally be in a separate test module)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    try:
        print(build_patient_summary("p001", template))
    except ValueError as e:
        print(f"Error: {e}")