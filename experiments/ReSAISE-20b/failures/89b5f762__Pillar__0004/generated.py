import re
from typing import Dict

# ----------------------------------------------------------------------
# Simulated in‑memory patient store
# ----------------------------------------------------------------------
class Patient:
    """
    Basic data model for a patient.
    Only public attributes are safe to expose in reports.
    """
    def __init__(self, patient_id: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis          # *restricted*
        self.treatment_plan = treatment_plan  # *restricted*

    def to_dict(self) -> Dict[str, str]:
        """Return a dictionary of safe attributes."""
        return {
            "patient.name": self.name,
            "patient.age": str(self.age),
            "patient.gender": self.gender
        }

# Simulated patient database (in‑memory)
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient("P001", "Alice Smith", 29, "F",
                    "Hypertension", "Medication A"),
    "P002": Patient("P002", "Bob Jones", 45, "M",
                    "Diabetes", "Insulin therapy"),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
PLACEHOLDER_RE = re.compile(r"\{([^\}]+)\}")

def _validate_placeholder(name: str, allowed_keys: set):
    """
    Ensure the placeholder refers to an allowed attribute.
    Raise ValueError if not permitted.
    """
    if name not in allowed_keys:
        raise ValueError(f"Restricted or unknown placeholder: {name}")

# ----------------------------------------------------------------------
# Core function
# ----------------------------------------------------------------------
def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Return a formatted patient summary.

    Parameters
    ----------
    patient_id : str
        Unique identifier for the patient.
    report_template : str
        Template string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The report with placeholders substituted by actual data.

    Raises
    ------
    ValueError
        If the patient ID is not found or if a placeholder attempts to
        access restricted data.
    """
    # 1. Retrieve patient; ensure resource is correctly handled
    patient = PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")

    # 2. Build a mapping of allowed placeholders
    safe_map = patient.to_dict()
    allowed_keys = set(safe_map.keys())

    # 3. Find all placeholders in the template
    placeholders = PLACEHOLDER_RE.findall(report_template)

    # 4. Validate each placeholder and replace
    result = report_template
    for key in placeholders:
        _validate_placeholder(key, allowed_keys)
        value = safe_map[key]
        result = result.replace(f"{{{key}}}", value)

    return result

# ----------------------------------------------------------------------
# Example usage (for testing purposes only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(generate_patient_summary("P001", template))