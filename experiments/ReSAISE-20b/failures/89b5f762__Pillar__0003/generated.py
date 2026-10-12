import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------------- #
# Domain model
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str


# --------------------------------------------------------------------------- #
# In‑memory store (for demonstration purposes)
# --------------------------------------------------------------------------- #

class PatientStore:
    """Thread‑safe in‑memory patient repository."""
    _patients: Dict[str, Patient] = {}

    @classmethod
    def add_patient(cls, patient: Patient) -> None:
        cls._patients[patient.id] = patient

    @classmethod
    def get_patient(cls, patient_id: str) -> Patient:
        if patient_id not in cls._patients:
            raise ValueError(f"Patient ID '{patient_id}' is invalid.")
        return cls._patients[patient_id]


# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

_RE_PLACEHOLDER = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _validate_template_placeholders(template: str, patient_attrs: set) -> None:
    """
    Ensure that all placeholders refer to allowed attributes.
    Raise ValueError if a restricted attribute is requested.
    """
    for match in _RE_PLACEHOLDER.finditer(template):
        attr = match.group(1)
        if attr not in patient_attrs:
            raise ValueError(f"Access to restricted attribute '{attr}' is forbidden.")


def _safe_format(template: str, mapping: Dict[str, str]) -> str:
    """
    Replace placeholders in the form {patient.<attr>} with values from mapping.
    This implementation avoids executing arbitrary code or accessing
    attributes that are not explicitly provided in the mapping.
    """
    def replacer(match):
        key = match.group(1)
        return str(mapping.get(key, f"{{{match.group(0)}}}"))  # leave unchanged if missing

    return _RE_PLACEHOLDER.sub(replacer, template)


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by filling the provided template with
    patient data.

    Parameters:
        patient_id (str): Unique identifier of the patient.
        report_template (str): Template containing placeholders like
                               '{patient.name}' or '{patient.age}'.

    Returns:
        str: The filled report string.

    Raises:
        ValueError: If the patient ID is invalid or if a restricted
                    attribute is requested in the template.
    """
    # Retrieve patient data (may raise ValueError for invalid ID)
    patient = PatientStore.get_patient(patient_id)

    # Convert patient dataclass to a dictionary of attributes
    patient_dict = asdict(patient)
    # Exclude the 'id' field from template substitution
    patient_dict.pop('id', None)

    # Validate that the template does not request restricted fields
    allowed_attrs = set(patient_dict.keys())
    _validate_template_placeholders(report_template, allowed_attrs)

    # Perform safe substitution
    summary = _safe_format(report_template, patient_dict)
    return summary


# --------------------------------------------------------------------------- #
# Example usage (this section would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Populate the store with a sample patient
    PatientStore.add_patient(
        Patient(
            id="P12345",
            name="John Doe",
            age=42,
            gender="Male",
            diagnosis="Hypertension",
            treatment_plan="Daily medication and lifestyle changes"
        )
    )

    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )

    try:
        report = generate_patient_summary("P12345", template)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")