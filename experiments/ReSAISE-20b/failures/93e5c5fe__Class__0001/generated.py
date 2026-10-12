import re
from dataclasses import dataclass, fields
from typing import Dict

# ----- Patient model ---------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    diagnosis: str          # sensitive
    treatment_plan: str     # sensitive


# ----- In‑memory patient store ---------------------------------------------

# Example data – in a real system this would be fetched from a database
PATIENT_STORE: Dict[str, Patient] = {
    "12345": Patient(
        uid="12345",
        name="John Doe",
        age=42,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Beta blockers"
    ),
    "67890": Patient(
        uid="67890",
        name="Jane Smith",
        age=29,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler therapy"
    ),
}


# ----- Helper functions -----------------------------------------------------

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}


def _extract_placeholders(template: str) -> set:
    """
    Return a set of placeholder names found in the template.
    Uses the same parsing rules as str.format().
    """
    pattern = r"{([^{}]+)}"
    placeholders = set()
    for match in re.finditer(pattern, template):
        # Handle nested braces like {{ and }}
        key = match.group(1).strip()
        if key:
            placeholders.add(key)
    return placeholders


def _allowed_fields(patient: Patient) -> Dict[str, str]:
    """
    Return a dictionary mapping field names to string values for
    non‑sensitive fields of the patient.
    """
    result = {}
    for f in fields(patient):
        if f.name not in _SENSITIVE_FIELDS:
            value = getattr(patient, f.name)
            result[f"name"] = str(value)  # 'name' is a placeholder name
    return {f.name: getattr(patient, f.name) for f in fields(patient)
            if f.name not in _SENSITIVE_FIELDS}


# ----- Main function --------------------------------------------------------

def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report from the given schema.

    Parameters
    ----------
    patient_uid : str
        The unique identifier of the patient.
    report_schema : str
        A string template containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string with non-sensitive patient data.

    Raises
    ------
    ValueError
        If the patient UID is unknown, or if the schema attempts to access
        sensitive fields (diagnosis or treatment_plan).
    """
    # Lookup patient
    patient = PATIENT_STORE.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient UID '{patient_uid}' not found.")

    # Parse placeholders
    placeholders = _extract_placeholders(report_schema)

    # Validate that no sensitive fields are requested
    for placeholder in placeholders:
        # Expected format: 'patient.fieldname'
        if not placeholder.startswith("patient."):
            raise ValueError(f"Invalid placeholder '{placeholder}'. "
                             f"Only 'patient.<field>' allowed.")
        field_name = placeholder.split(".", 1)[1]
        if field_name in _SENSITIVE_FIELDS:
            raise ValueError(f"Attempt to expose sensitive data: "
                             f"'{field_name}' is not allowed.")

    # Prepare context for formatting
    context = {"patient": _allowed_fields(patient)}

    try:
        report = report_schema.format(**context)
    except KeyError as exc:
        # Missing field in the context
        raise ValueError(f"Missing data for placeholder: {exc}") from None

    return report


# ----- Example usage --------------------------------------------------------

if __name__ == "__main__":
    schema = "Patient {patient.name}, age {patient.age}, gender {patient.gender}."
    print(compose_patient_report("12345", schema))