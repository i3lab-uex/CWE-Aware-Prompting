import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# 1. Patient model and in‑memory repository (simulating a database)
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# A simple in‑memory patient store. In a real system this would be
# replaced by database access logic that handles connection pooling,
# transactions, etc.
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        patient_id="p001",
        name="Alice Smith",
        age=30,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "p002": Patient(
        patient_id="p002",
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------------- #
# 2. Whitelist of safe fields that may appear in the template
# --------------------------------------------------------------------------- #

_ALLOWED_FIELDS = {
    "patient.name",
    "patient.age",
    "patient.gender",
    "patient.diagnosis",
    "patient.treatment_plan",
}

# --------------------------------------------------------------------------- #
# 3. Helper to safely extract values from a Patient instance
# --------------------------------------------------------------------------- #

def _extract_patient_value(patient: Patient, key: str) -> str:
    """
    Extracts the value for a given placeholder key from the patient.
    Raises ValueError if the key is not allowed.
    """
    if key not in _ALLOWED_FIELDS:
        raise ValueError(f"Attempt to access restricted field '{key}'.")
    # Map the key to an attribute on the Patient instance
    attr_name = key.split(".")[1]
    value = getattr(patient, attr_name)
    return str(value)

# --------------------------------------------------------------------------- #
# 4. Main function: build_patient_summary
# --------------------------------------------------------------------------- #

def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Generates a personalized patient summary by replacing placeholders
    in the report_template with actual data from the Patient record.

    Parameters
    ----------
    identifier : str
        The unique patient ID.
    report_template : str
        A string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The fully rendered report string.

    Raises
    ------
    ValueError
        If the patient ID is unknown or a placeholder references a restricted field.
    """
    # ----------------------------------------------------------------------- #
    # 4.1 Validate patient ID and load the Patient instance
    # ----------------------------------------------------------------------- #
    if not isinstance(identifier, str) or not identifier:
        raise ValueError("Patient ID must be a non-empty string.")

    # Simulate a resource acquisition (e.g., DB connection) with context
    patient = None
    try:
        # In a real system this could be a DB session context manager.
        patient = _PATIENT_DB.get(identifier)
        if patient is None:
            raise ValueError(f"Unknown patient ID: {identifier}")
    finally:
        # Resource cleanup placeholder (no-op here, but demonstrates pattern)
        pass

    # ----------------------------------------------------------------------- #
    # 4.2 Find all placeholders in the template
    # ----------------------------------------------------------------------- #
    placeholder_pattern = re.compile(r"\{([^}]+)\}")
    placeholders = set(placeholder_pattern.findall(report_template))

    # ----------------------------------------------------------------------- #
    # 4.3 Validate placeholders against whitelist
    # ----------------------------------------------------------------------- #
    for ph in placeholders:
        if ph not in _ALLOWED_FIELDS:
            raise ValueError(f"Invalid or restricted placeholder: {ph}")

    # ----------------------------------------------------------------------- #
    # 4.4 Perform safe substitution
    # ----------------------------------------------------------------------- #
    def replacement(match: re.Match) -> str:
        key = match.group(1)
        return _extract_patient_value(patient, key)

    rendered_report = placeholder_pattern.sub(replacement, report_template)
    return rendered_report

# --------------------------------------------------------------------------- #
# 5. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}"
    )
    try:
        report = build_patient_summary("p001", template)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")