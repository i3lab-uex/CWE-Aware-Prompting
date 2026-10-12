import re
from typing import Dict, Any

# ----------------------------------------------------------------------
# Simulated patient storage (in a real system this would be a DB or API)
# ----------------------------------------------------------------------
class Patient:
    """
    Simple patient data model.
    Only a subset of attributes are considered safe for reporting.
    """
    _allowed_attrs = {"name", "age", "gender", "diagnosis"}

    def __init__(self, patient_id: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.diagnosis = diagnosis
        # treatment_plan is considered restricted and not exposed in reports
        self.treatment_plan = treatment_plan

    def get_allowed_data(self) -> Dict[str, Any]:
        """Return a dict of attributes that are allowed to be used in reports."""
        return {attr: getattr(self, attr) for attr in self._allowed_attrs}


# In‑memory patient registry
PATIENT_REGISTRY: Dict[str, Patient] = {
    "patient-001": Patient(
        patient_id="patient-001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "patient-002": Patient(
        patient_id="patient-002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, Avoid triggers"
    ),
}


# ----------------------------------------------------------------------
# Core functionality
# ----------------------------------------------------------------------
PLACEHOLDER_PATTERN = re.compile(r"\{(?P<path>patient\.[a-zA-Z_][a-zA-Z0-9_]*)\}")

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a patient report by substituting placeholders in the template.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier of the patient.
    template_string : str
        Template containing placeholders like {patient.name}.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or a restricted attribute is referenced.
    """
    # 1. Retrieve patient data
    patient = PATIENT_REGISTRY.get(patient_identifier)
    if not patient:
        raise ValueError(f"Invalid patient identifier: {patient_identifier}")

    # 2. Prepare a safe data mapping
    allowed_data = patient.get_allowed_data()

    # 3. Find all placeholders in the template
    def replace_placeholder(match: re.Match) -> str:
        full_path = match.group("path")  # e.g. patient.name
        _, attr_name = full_path.split(".", 1)

        if attr_name not in allowed_data:
            raise ValueError(
                f"Attempt to access restricted or unknown attribute '{attr_name}' "
                "in patient report."
            )
        # Convert value to string (handles None, etc.)
        return str(allowed_data[attr_name])

    # 4. Perform substitution
    try:
        report = PLACEHOLDER_PATTERN.sub(replace_placeholder, template_string)
    except re.error as exc:
        raise ValueError(f"Invalid template syntax: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
    )
    print(build_patient_report("patient-001", template))