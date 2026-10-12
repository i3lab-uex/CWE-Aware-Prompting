import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------
# Patient model and in‑memory store (for demo purposes)
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    # Sensitive fields – should never be exposed via report_template
    diagnosis: str
    treatment_plan: str

# Example patient store (in a real system this would be a database)
PATIENT_STORE: Dict[str, Patient] = {
    "001": Patient(
        uid="001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication",
    ),
    "002": Patient(
        uid="002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy",
    ),
}

# --------------------------------------------------------------------
# Helper utilities
# --------------------------------------------------------------------

SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
PLACEHOLDER_PATTERN = re.compile(r"\{([^{}]+)\}")

def _get_patient(uid: str) -> Patient:
    """
    Retrieve a patient by UID from the store.
    Raise ValueError if not found.
    """
    try:
        return PATIENT_STORE[uid]
    except KeyError as exc:
        raise ValueError(f"Patient with UID '{uid}' not found.") from exc

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference any sensitive fields.
    Raise ValueError if it does.
    """
    for match in PLACEHOLDER_PATTERN.finditer(template):
        field = match.group(1).strip()
        # Allow only 'patient.<field>' syntax
        if not field.startswith("patient."):
            raise ValueError(f"Unsupported placeholder '{match.group(0)}'.")
        attr = field.split(".", 1)[1]
        if attr in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{attr}' is prohibited.")

def _build_context(patient: Patient) -> Dict[str, str]:
    """
    Create a mapping of placeholder names to string values.
    Only non-sensitive attributes are included.
    """
    context = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender,
    }
    return context

# --------------------------------------------------------------------
# Main function
# --------------------------------------------------------------------

def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report string from the provided template.

    Parameters
    ----------
    patient_uid : str
        The unique identifier for the patient.
    report_schema : str
        A string template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string containing only non-sensitive patient data.

    Raises
    ------
    ValueError
        If the patient UID is not found, or if the template attempts to access
        sensitive fields (diagnosis or treatment_plan), or contains unsupported
        placeholders.
    """
    # Validate the template first to avoid partial formatting errors
    _validate_template(report_schema)

    # Retrieve patient record
    patient = _get_patient(patient_uid)

    # Build safe context and format the template
    context = _build_context(patient)
    try:
        return report_schema.format(**context)
    except KeyError as exc:
        # This should not happen if validation passed, but guard against it
        raise ValueError(f"Missing placeholder in context: {exc}") from exc

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------

# if __name__ == "__main__":
#     template = "Patient {patient.name}, age {patient.age}, gender: {patient.gender}."
#     print(compose_patient_report("001", template))