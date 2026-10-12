import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------- Data Layer ---------------------------------

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Restricted data
    treatment_plan: str     # Restricted data

# In‑memory patient store (simulates a database)
PATIENT_STORE: Dict[str, Patient] = {
    "p001": Patient(
        patient_id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "p002": Patient(
        patient_id="p002",
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Diabetes Type II",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------- Utility -----------------------------------

_RE_PLACEHOLDER = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# Fields that are considered sensitive and must not be exposed
RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}


def _get_patient(patient_id: str) -> Patient:
    """Retrieve a patient record, raising ValueError if not found."""
    patient = PATIENT_STORE.get(patient_id)
    if patient is None:
        raise ValueError(f"Patient ID '{patient_id}' does not exist.")
    return patient


def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference restricted fields.
    Raises ValueError if it does.
    """
    for match in _RE_PLACEHOLDER.finditer(template):
        field = match.group(1)
        if field in RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field}' is not allowed.")


def _populate_template(template: str, patient: Patient) -> str:
    """
    Replace placeholders with actual patient data.
    Only fields defined on the Patient dataclass are allowed.
    """
    def replacer(match):
        field_name = match.group(1)
        # Using asdict ensures only defined fields are accessed
        patient_dict = asdict(patient)
        if field_name not in patient_dict:
            raise ValueError(f"Unknown placeholder '{field_name}'.")
        return str(patient_dict[field_name])

    return _RE_PLACEHOLDER.sub(replacer, template)


# --------------------------- Public API ---------------------------------

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a patient report by filling in placeholders from the template.

    Args:
        patient_identifier (str): Unique ID of the patient.
        template_string (str): Template containing placeholders like
                               '{patient.name}', '{patient.age}'.

    Returns:
        str: The populated report string.

    Raises:
        ValueError: If the patient ID is invalid or if restricted data
                    is requested in the template.
    """
    # Validate template before accessing patient data
    _validate_template(template_string)

    # Retrieve the patient record safely
    patient = _get_patient(patient_identifier)

    # Populate and return the report
    return _populate_template(template_string, patient)


# --------------------------- Example Usage --------------------------------

if __name__ == "__main__":
    tmpl = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    try:
        report = build_patient_report("p001", tmpl)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")