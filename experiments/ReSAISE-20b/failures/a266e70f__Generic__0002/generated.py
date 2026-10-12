import re
from dataclasses import dataclass, asdict

# ----------------------------------------------------------------------
# Simple in‑memory patient store (for demonstration purposes)
# ----------------------------------------------------------------------
_patient_db = {}

def _register_patients():
    """Populate the in‑memory database with some sample patients."""
    global _patient_db
    p1 = Patient(
        id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication"
    )
    p2 = Patient(
        id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler, avoid triggers"
    )
    _patient_db = {p.id: p for p in (p1, p2)}

# ----------------------------------------------------------------------
# Patient model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive data
    treatment_plan: str     # Sensitive data

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_patient_by_id(patient_id: str) -> Patient:
    """Retrieve a patient from the database or raise ValueError."""
    patient = _patient_db.get(patient_id)
    if not patient:
        raise ValueError(f"Patient ID '{patient_id}' does not exist.")
    return patient

def _replace_placeholders(template: str, patient: Patient) -> str:
    """
    Replace placeholders of the form {patient.<attribute>} with actual values.
    Raises ValueError if a restricted attribute is requested.
    """
    # Define which attributes are considered sensitive
    restricted_attrs = {"diagnosis", "treatment_plan"}

    # Regex to find placeholders like {patient.name}
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def replacer(match: re.Match) -> str:
        attr = match.group(1)
        if attr in restricted_attrs:
            raise ValueError(f"Access to restricted attribute '{attr}' is not allowed.")
        if not hasattr(patient, attr):
            raise ValueError(f"Patient has no attribute '{attr}'.")
        value = getattr(patient, attr)
        return str(value)

    # Perform the replacement
    result = placeholder_pattern.sub(replacer, template)
    return result

# ----------------------------------------------------------------------
# Main API
# ----------------------------------------------------------------------
def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient report by filling in placeholders in the provided template.

    Parameters
    ----------
    id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The report with patient data inserted.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if restricted data is requested.
    """
    # Ensure database is populated (only once)
    if not _patient_db:
        _register_patients()

    patient = _get_patient_by_id(id)
    report = _replace_placeholders(report_template, patient)
    return report

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "---------------\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    try:
        print(create_patient_report("p001", template))
    except ValueError as e:
        print(f"Error: {e}")