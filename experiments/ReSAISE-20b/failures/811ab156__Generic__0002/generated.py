import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Mock patient database and restricted fields
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """Simple representation of a patient record."""
    identifier: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Restricted field – not allowed in public reports
    treatment_plan: str

# Example patient registry. In a real system this would be replaced by
# database access logic.
_PATIENT_REGISTRY: Dict[str, Patient] = {
    "P001": Patient(
        identifier="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication X"
    ),
    "P002": Patient(
        identifier="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy, diet modification"
    ),
}

# Fields that are considered restricted and must not appear in public
# reports. Attempting to reference them raises a ValueError.
_RESTRICTED_FIELDS = {"diagnosis"}

# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------

def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Assemble a personalized patient report by replacing placeholders in
    `report_template` with the corresponding attributes of the patient.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier for the patient.
    report_template : str
        Report template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is not found or if a restricted field is referenced.
    """
    # --------------------------------------------------------------------
    # 1. Retrieve patient record
    # --------------------------------------------------------------------
    patient = _PATIENT_REGISTRY.get(patient_identifier)
    if not patient:
        raise ValueError(f"Invalid patient identifier: {patient_identifier!r}")

    # --------------------------------------------------------------------
    # 2. Detect placeholders
    # --------------------------------------------------------------------
    placeholder_pattern = re.compile(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}")
    matches = placeholder_pattern.findall(report_template)

    # --------------------------------------------------------------------
    # 3. Validate placeholders
    # --------------------------------------------------------------------
    for field_name in set(matches):
        if field_name not in Patient.__annotations__:
            raise ValueError(f"Unknown patient attribute: {field_name!r}")
        if field_name in _RESTRICTED_FIELDS:
            raise ValueError(f"Access to restricted field '{field_name}' is prohibited")

    # --------------------------------------------------------------------
    # 4. Perform substitution
    # --------------------------------------------------------------------
    def replacer(match: re.Match) -> str:
        field = match.group(1)
        value = getattr(patient, field)
        return str(value)

    formatted_report = placeholder_pattern.sub(replacer, report_template)

    # --------------------------------------------------------------------
    # 5. Return result
    # --------------------------------------------------------------------
    return formatted_report

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

# if __name__ == "__main__":
#     template = (
#         "Patient Report\n"
#         "Name: {patient.name}\n"
#         "Age: {patient.age}\n"
#         "Gender: {patient.gender}\n"
#         "Treatment Plan: {patient.treatment_plan}"
#     )
#     print(assemble_patient_report("P001", template))