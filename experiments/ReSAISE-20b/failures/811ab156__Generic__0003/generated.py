import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Mock data layer – in a real system this would query a database.
# ----------------------------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # Sensitive
    treatment_plan: str = field(repr=False)     # Sensitive

# Example patient records (normally stored securely in a DB)
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, lifestyle changes"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Diabetes Type II",
        treatment_plan="Insulin therapy, diet plan"
    ),
}

# ----------------------------------------------------------------------
# Utility functions
# ----------------------------------------------------------------------
def _get_patient(patient_id: str) -> Patient:
    """
    Retrieve a patient object from the mock database.
    Raises ValueError if the ID is not found.
    """
    patient = _PATIENT_DB.get(patient_id)
    if patient is None:
        raise ValueError(f"Invalid patient identifier: {patient_id!r}")
    return patient


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def assemble_patient_report(patient_identifier: str, report_template: str) -> str:
    """
    Assemble a personalized patient report by substituting placeholders in
    `report_template` with data from the specified patient.

    Allowed placeholder fields: name, age, gender.
    Attempts to access restricted fields (diagnosis, treatment_plan)
    will raise a ValueError.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier of the patient.
    report_template : str
        Report template containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if restricted information is requested.
    """
    # 1. Retrieve patient data
    patient = _get_patient(patient_identifier)

    # 2. Extract placeholders from the template
    placeholder_pattern = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(report_template)

    # 3. Build context dictionary for allowed fields only
    allowed_fields = {"name", "age", "gender"}
    context: Dict[str, str] = {}

    for field_name in placeholders:
        if field_name not in allowed_fields:
            raise ValueError(
                f"Access to restricted patient information '{field_name}' is not allowed."
            )
        # Use getattr to fetch the attribute
        context[field_name] = str(getattr(patient, field_name))

    # 4. Perform substitution
    try:
        formatted_report = report_template.format(patient=context)
    except KeyError as exc:
        # This should not happen because we pre-validated placeholders,
        # but catch just in case.
        raise ValueError(f"Missing placeholder data for {exc}") from exc

    return formatted_report


# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(assemble_patient_report("P001", template))