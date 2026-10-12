import re
from typing import Dict

# ------------------------------------------------------------------
# Simple in‑memory patient database (for demonstration purposes)
# ------------------------------------------------------------------

class Patient:
    """
    A minimal representation of a patient record.
    """
    def __init__(self, id: str, name: str, age: int, gender: str,
                 diagnosis: str, treatment_plan: str):
        self.id = id
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis          # highly sensitive
        self.treatment_plan = treatment_plan  # highly sensitive


# Example patient records (in a real system this would be stored in a secure DB)
PATIENT_DB: Dict[str, Patient] = {
    "patient-001": Patient(
        id="patient-001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication"
    ),
    "patient-002": Patient(
        id="patient-002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes Type 2",
        treatment_plan="Insulin therapy"
    ),
}


# ------------------------------------------------------------------
# Allowed placeholders – any attempt to access restricted data will
# raise a ValueError.  This mitigates CWE‑200 (information exposure).
# ------------------------------------------------------------------
ALLOWED_PLACEHOLDERS = {
    "patient.name",
    "patient.age",
    "patient.gender"
}


# ------------------------------------------------------------------
# Core function
# ------------------------------------------------------------------
def create_patient_report(id: str, report_template: str) -> str:
    """
    Generates a patient report by substituting placeholders in the
    template with actual patient data.

    Parameters
    ----------
    id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string with placeholders replaced.

    Raises
    ------
    ValueError
        If the patient ID is not found or if a restricted placeholder
        is used in the template.
    """
    # Retrieve patient record
    patient = PATIENT_DB.get(id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {id}")

    # Find all placeholders in the template
    placeholders = set(re.findall(r"{([^}]+)}", report_template))

    # Check that all placeholders are allowed
    for ph in placeholders:
        if ph not in ALLOWED_PLACEHOLDERS:
            raise ValueError(f"Access to restricted data '{ph}' is not allowed")

    # Prepare a mapping of placeholder -> value
    context = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender
    }

    # Replace placeholders
    def _replace(match):
        key = match.group(1)
        return context.get(key, "")

    result = re.sub(r"{([^}]+)}", _replace, report_template)
    return result


# ------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("patient-001", template))