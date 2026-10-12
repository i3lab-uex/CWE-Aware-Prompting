import re
from dataclasses import dataclass
from typing import Dict

# ---------- Domain model ----------
@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    pat_id: str
    name: str
    age: int
    gender: str
    # Sensitive fields – only privileged users may access them.
    diagnosis: str
    treatment_plan: str

# ---------- In‑memory repository ----------
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        pat_id="P001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication",
    ),
    "P002": Patient(
        pat_id="P002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy, diet plan",
    ),
}

# ---------- Utility ----------
_RE_PLACEHOLDER = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

# Fields that are considered sensitive and must not be exposed
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}

def _get_patient(pat_id: str) -> Patient:
    """Retrieve a patient record or raise an error if not found."""
    try:
        return PATIENT_DB[pat_id]
    except KeyError as exc:
        raise ValueError(f"Invalid patient ID: {pat_id}") from exc

def _extract_placeholders(layout: str) -> set:
    """Return a set of placeholder field names found in the layout."""
    return {m.group(1) for m in _RE_PLACEHOLDER.finditer(layout)}

def create_patient_report(pat_id: str, layout: str) -> str:
    """
    Generate a personalized report for the given patient.

    Parameters
    ----------
    pat_id : str
        Unique identifier of the patient.
    layout : str
        Template string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string with placeholders replaced by patient data.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if the template tries to access restricted fields.
    """
    # Retrieve patient
    patient = _get_patient(pat_id)

    # Identify placeholders in the template
    placeholders = _extract_placeholders(layout)

    # Ensure no restricted fields are requested
    if any(field in _SENSITIVE_FIELDS for field in placeholders):
        raise ValueError("Attempt to access restricted medical information")

    # Build a mapping for allowed fields
    patient_dict = {
        "name": patient.name,
        "age": str(patient.age),
        "gender": patient.gender,
    }

    # Perform safe substitution
    def replace(match):
        field = match.group(1)
        if field not in patient_dict:
            raise ValueError(f"Unknown placeholder: {field}")
        return patient_dict[field]

    report = _RE_PLACEHOLDER.sub(replace, layout)
    return report

# ---------- Example usage ----------
if __name__ == "__main__":
    template = (
        "Patient Report\n"
        "---------------\n"
        "Name   : {patient.name}\n"
        "Age    : {patient.age}\n"
        "Gender : {patient.gender}\n"
    )
    print(create_patient_report("P001", template))