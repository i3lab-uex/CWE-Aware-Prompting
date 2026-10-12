import re
from dataclasses import dataclass, field

# --------------------------------------------------------------------------- #
# Data model and in‑memory store
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    """Represents a patient record in the system."""
    id: str
    name: str
    age: int
    gender: str
    # Restricted fields – should never be exposed via a public report
    diagnosis: str = field(repr=False, default="")          # Sensitive
    treatment_plan: str = field(repr=False, default="")   # Sensitive


# A simple in‑memory database of patients
_PATIENT_DB = {
    "p001": Patient(
        id="p001",
        name="Alice Smith",
        age=34,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication",
    ),
    "p002": Patient(
        id="p002",
        name="Bob Johnson",
        age=58,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy, diet control",
    ),
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_patient_by_id(patient_id: str) -> Patient:
    """Retrieve a patient from the store, raising ValueError if not found."""
    patient = _PATIENT_DB.get(patient_id)
    if patient is None:
        raise ValueError(f"Patient ID '{patient_id}' does not exist.")
    return patient


# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #

def create_patient_report(id: str, report_template: str) -> str:
    """
    Generate a patient‑specific report by filling in placeholders
    within *report_template* with data from the patient's record.

    Placeholders must be of the form `{patient.<attribute>}`.
    Only non‑restricted attributes (`name`, `age`, `gender`) are
    allowed. Attempting to access restricted data raises ValueError.

    Parameters
    ----------
    id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders.

    Returns
    -------
    str
        The report with all placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if restricted data is requested.
    """
    # 1. Fetch the patient
    patient = _get_patient_by_id(id)

    # 2. Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(report_template)

    # 3. Validate placeholders and build a mapping of allowed attributes
    allowed_attrs = {"name", "age", "gender"}
    patient_data: dict[str, str | int] = {}
    for attr in placeholders:
        if attr not in allowed_attrs:
            raise ValueError(
                f"Access to restricted patient attribute '{attr}' is not allowed."
            )
        # Use getattr safely; all allowed attrs exist on Patient
        patient_data[attr] = getattr(patient, attr)

    # 4. Perform the substitution
    def replace_match(match: re.Match) -> str:
        attr_name = match.group(1)
        return str(patient_data[attr_name])

    report = placeholder_pattern.sub(replace_match, report_template)

    return report


# --------------------------------------------------------------------------- #
# Example usage (for testing only – remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("p001", template))