import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------
# Mock patient database
# ------------------------------

@dataclass
class Patient:
    """Simple data holder for patient information."""
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# Example patients (in a real system this would be replaced by a DB query)
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="Alice Smith",
        age=34,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication, lifestyle changes"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Bob Johnson",
        age=58,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ------------------------------
# Build patient report
# ------------------------------

# Only expose these attributes to the template.
ALLOWED_ATTRIBUTES = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan",
}

PLACEHOLDER_RE = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a patient report by filling placeholders in `template_string`
    with the patient's data.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier of a patient.
    template_string : str
        A string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The rendered report string.

    Raises
    ------
    ValueError
        If the patient ID does not exist or if a restricted attribute is accessed.
    """
    # Retrieve patient
    patient = PATIENT_DB.get(patient_identifier)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_identifier}")

    # Function to replace each placeholder
    def _replace(match):
        attr = match.group(1)
        if attr not in ALLOWED_ATTRIBUTES:
            raise ValueError(f"Access to restricted attribute '{attr}' is forbidden.")
        return str(getattr(patient, attr))

    # Perform substitution
    try:
        result = PLACEHOLDER_RE.sub(_replace, template_string)
    except re.error as exc:
        # Catch regex errors (unlikely but defensive)
        raise ValueError(f"Template processing error: {exc}") from exc

    return result


# ------------------------------
# Example usage (uncomment to test)
# ------------------------------

if __name__ == "__main__":
    tmpl = (
        "Patient Report\n"
        "--------------\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
        "Diagnosis: {patient.diagnosis}\n"
        "Treatment Plan: {patient.treatment_plan}\n"
    )
    print(build_patient_report("P001", tmpl))