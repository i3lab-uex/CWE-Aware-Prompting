import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Sample Patient model – in a real system this would come from the
# database layer or an ORM.
# --------------------------------------------------------------------
@dataclass
class Patient:
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# --------------------------------------------------------------------
# In‑memory patient store for demonstration purposes.
# Replace this with real persistence in production.
# --------------------------------------------------------------------
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
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy",
    ),
}

# --------------------------------------------------------------------
# Restricted fields that should not be exposed without explicit
# authorization.  In this simplified example we assume the caller is
# not authorized for any restricted fields.
# --------------------------------------------------------------------
_RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

PLACEHOLDER_PATTERN = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")


def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Build a personalized patient summary from a template.

    Parameters
    ----------
    identifier : str
        The unique patient identifier.
    report_template : str
        A string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The formatted report with placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID does not exist or if a restricted field is requested.
    """
    # ------------------------------------------------------------
    # Retrieve patient record
    # ------------------------------------------------------------
    patient = _PATIENT_DB.get(identifier)
    if not patient:
        raise ValueError(f"Invalid patient identifier: {identifier}")

    # ------------------------------------------------------------
    # Validate placeholders for restricted access
    # ------------------------------------------------------------
    placeholders = PLACEHOLDER_PATTERN.findall(report_template)
    if any(field in _RESTRICTED_FIELDS for field in placeholders):
        raise ValueError("Attempt to access restricted medical information")

    # ------------------------------------------------------------
    # Build a mapping for format operation
    # ------------------------------------------------------------
    patient_dict = {
        "name": patient.name,
        "age": str(patient.age),
        "gender": patient.gender,
    }

    # ------------------------------------------------------------
    # Perform substitution safely
    # ------------------------------------------------------------
    def replacement(match: re.Match) -> str:
        field_name = match.group(1)
        return patient_dict.get(field_name, f"{{unknown:{field_name}}}")

    formatted_report = PLACEHOLDER_PATTERN.sub(replacement, report_template)
    return formatted_report


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(build_patient_summary("p001", template))