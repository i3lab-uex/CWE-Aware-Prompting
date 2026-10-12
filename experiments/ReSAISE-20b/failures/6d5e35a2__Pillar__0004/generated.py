import re
from typing import Dict

# Simulated in‑memory patient database.
class Patient:
    def __init__(self, pat_id: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.pat_id = pat_id
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis          # restricted field
        self.treatment_plan = treatment_plan  # restricted field

# Example data – in a real system this would come from a secure database.
PATIENT_DB: Dict[str, Patient] = {
    "001": Patient("001", "Alice Smith", 29, "F",
                   "Hypertension", "Lifestyle changes"),
    "002": Patient("002", "Bob Jones", 45, "M",
                   "Type II Diabetes", "Metformin"),
}

# Fields that are allowed to be exposed in a report.
ALLOWED_FIELDS = {
    "patient.name",
    "patient.age",
    "patient.gender",
}

PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")

def _get_patient(pat_id: str) -> Patient:
    """
    Retrieve a patient from the database.

    Raises:
        ValueError: If no patient exists with the given ID.
    """
    patient = PATIENT_DB.get(pat_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {pat_id}")
    return patient

def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized report for the given patient.

    Args:
        pat_id: The unique identifier of the patient.
        layout: A string containing placeholders like `{patient.name}`.

    Returns:
        The formatted report as a string.

    Raises:
        ValueError: If the patient ID is invalid or if restricted
                    information is requested.
    """
    # Fetch patient once; no lingering resources.
    patient = _get_patient(pat_id)

    def replace(match: re.Match) -> str:
        placeholder = match.group(1)
        if placeholder not in ALLOWED_FIELDS:
            raise ValueError(f"Access to restricted field '{placeholder}' is denied.")
        # Resolve the attribute on the patient object.
        attr_name = placeholder.split(".")[1]
        value = getattr(patient, attr_name)
        return str(value)

    # Perform safe substitution.
    report = PLACEHOLDER_PATTERN.sub(replace, layout)
    return report

# Example usage:
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}"
    )
    print(create_patient_report("001", template))