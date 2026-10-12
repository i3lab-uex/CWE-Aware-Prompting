import re
from dataclasses import dataclass, field
from typing import Dict

# --- Data model -------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """Represents a patient in the system."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # Sensitive
    treatment_plan: str = field(repr=False)     # Sensitive


# --- In‑memory patient store -----------------------------------------------

# For demonstration purposes we use a simple dictionary.
# In a real application this would be replaced by a database or
# an external service.
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication",
    ),
    "p002": Patient(
        id="p002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy",
    ),
}


# --- Helper functions -------------------------------------------------------

def _get_patient_by_id(patient_id: str) -> Patient:
    """Retrieve a patient from the database or raise ValueError."""
    try:
        return _PATIENT_DB[patient_id]
    except KeyError as exc:
        raise ValueError(f"Invalid patient ID: {patient_id}") from exc


def _replace_placeholders(template: str, patient: Patient) -> str:
    """
    Replace placeholders of the form {patient.attribute} in *template*
    with the corresponding attribute from *patient*.

    Raises ValueError if an attempt is made to access restricted data.
    """
    # Allowed (non‑sensitive) attributes
    SAFE_ATTRIBUTES = {"name", "age", "gender"}

    # Regex to find placeholders like {patient.name}
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def _replacement(match: re.Match) -> str:
        attr_name = match.group(1)
        if attr_name not in SAFE_ATTRIBUTES:
            raise ValueError(f"Access to restricted attribute '{attr_name}' is prohibited.")
        return str(getattr(patient, attr_name))

    try:
        return placeholder_pattern.sub(_replacement, template)
    except ValueError as exc:
        raise


# --- Public API -------------------------------------------------------------

def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient report by filling in the *report_template* with
    information from the patient identified by *id*.

    Parameters
    ----------
    id : str
        Unique identifier of the patient.
    report_template : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The report with placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if restricted data is requested.
    """
    patient = _get_patient_by_id(id)
    return _replace_placeholders(report_template, patient)


# --- Example usage ----------------------------------------------------------

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("p001", template))