import re
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Mock data layer (in a real system this would interface with a database)
# --------------------------------------------------------------------------- #

class Patient:
    """Represents a patient record."""
    def __init__(self, identifier: str, name: str, age: int,
                 gender: str, diagnosis: str, treatment_plan: str):
        self.identifier = identifier
        self.name = name
        self.age = age
        self.gender = gender
        # Diagnosis and treatment plan are considered sensitive.
        self._diagnosis = diagnosis
        self._treatment_plan = treatment_plan

    @property
    def diagnosis(self) -> str:
        raise PermissionError("Access to diagnosis is restricted.")

    @property
    def treatment_plan(self) -> str:
        raise PermissionError("Access to treatment plan is restricted.")


# In‑memory patient store for demo purposes
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient("p001", "Alice Smith", 30, "F",
                    "Hypertension", "Lifestyle changes"),
    "p002": Patient("p002", "Bob Jones", 45, "M",
                    "Diabetes", "Insulin therapy"),
}


def _get_patient_by_id(patient_identifier: str) -> Patient:
    """Retrieve a patient instance by ID or raise ValueError."""
    patient = _PATIENT_DB.get(patient_identifier)
    if not patient:
        raise ValueError(f"Patient ID '{patient_identifier}' is invalid.")
    return patient


# --------------------------------------------------------------------------- #
# Report generation logic
# --------------------------------------------------------------------------- #

PLACEHOLDER_REGEX = re.compile(r"\{(?P<field>patient\.[a-z_]+)\}")

# Fields that are considered restricted and should not be exposed
_RESTRICTED_FIELDS = {"patient.diagnosis", "patient.treatment_plan"}


def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Generate a patient report by substituting placeholders in the template
    with data from the specified patient's record.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier of the patient.
    report_template : str
        Report template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The fully formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if a restricted field is accessed.
    """
    # 1. Retrieve the patient record
    patient = _get_patient_by_id(patient_identifier)

    # 2. Prepare a mapping of allowed fields to values
    field_map: Dict[str, Any] = {
        "patient.name": patient.name,
        "patient.age": patient.age,
        "patient.gender": patient.gender,
    }

    # 3. Validate placeholders in the template
    for match in PLACEHOLDER_REGEX.finditer(report_template):
        field = match.group("field")
        if field in _RESTRICTED_FIELDS:
            raise ValueError(f"Attempt to access restricted information: '{field}'.")
        if field not in field_map:
            raise ValueError(f"Unknown placeholder: '{field}'.")

    # 4. Perform safe substitution
    def replacer(match: re.Match) -> str:
        field = match.group("field")
        return str(field_map[field])

    formatted_report = PLACEHOLDER_REGEX.sub(replacer, report_template)
    return formatted_report


# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(assemble_patient_report("p001", template))