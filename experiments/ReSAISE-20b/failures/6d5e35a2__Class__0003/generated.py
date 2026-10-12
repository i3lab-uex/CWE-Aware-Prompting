import re
from typing import Dict

# Mock Patient data store for demonstration purposes.
# In a real system this would interface with a database or secure storage layer.
_PATIENT_DB: Dict[str, "Patient"] = {}

class Patient:
    """
    Represents a patient record.
    Only non-sensitive fields should be exposed via the reporting API.
    """
    def __init__(self, pat_id: str, name: str, age: int, gender: str,
                 diagnosis: str = None, treatment_plan: str = None):
        self.pat_id = pat_id
        self.name = name
        self.age = age
        self.gender = gender
        # Sensitive data that should not be exposed via the public API
        self._diagnosis = diagnosis
        self.treatment_plan = treatment_plan

    @property
    def diagnosis(self):
        """Diagnosis is considered sensitive and should not be exposed."""
        return self._diagnosis


# Populate the mock database with a sample patient.
_PATIENT_DB["12345"] = Patient(
    pat_id="12345",
    name="John Doe",
    age=35,
    gender="Male",
    diagnosis="Hypertension",
    treatment_plan="Lifestyle changes and medication."
)


def _sanitize_template(template: str) -> None:
    """
    Validate the template to ensure it does not request restricted data.
    Raises ValueError if a forbidden placeholder is found.
    """
    # Allowed placeholders
    allowed = {"patient.name", "patient.age", "patient.gender",
               "patient.treatment_plan"}
    # Find all placeholders of the form {patient.<field>}
    placeholders = set(re.findall(r"\{([^{}]+)\}", template))
    for ph in placeholders:
        if ph not in allowed:
            raise ValueError(f"Unauthorized access to restricted field: {ph}")


def _get_patient(pat_id: str) -> Patient:
    """
    Retrieve a patient from the database.
    Raises ValueError if the ID is not found.
    """
    patient = _PATIENT_DB.get(pat_id)
    if patient is None:
        raise ValueError(f"Invalid patient ID: {pat_id}")
    return patient


def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized report for the given patient.

    Parameters
    ----------
    pat_id : str
        Unique identifier of the patient.
    layout : str
        Report template containing placeholders such as
        '{patient.name}', '{patient.age}', etc.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if the template attempts to access
        restricted medical information.
    """
    # Step 1: Validate the template for restricted placeholders
    _sanitize_template(layout)

    # Step 2: Retrieve patient record securely
    patient = _get_patient(pat_id)

    # Step 3: Build a mapping for placeholder substitution
    context = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender,
        "patient.treatment_plan": patient.treatment_plan or "",
    }

    # Step 4: Perform safe substitution
    def replace(match):
        key = match.group(1)
        return context.get(key, f"{{{key}}}")  # leave unchanged if missing

    report = re.sub(r"\{([^{}]+)\}", replace, layout)

    return report