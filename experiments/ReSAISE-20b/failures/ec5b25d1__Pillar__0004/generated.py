import re
from dataclasses import dataclass, asdict
from typing import Dict

# --------------------------------------------------------------------
# Domain model --------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    code: str
    name: str
    age: int
    gender: str
    diagnosis: str          # sensitive
    treatment_plan: str     # sensitive


# --------------------------------------------------------------------
# In‑memory patient database -----------------------------------------
# In a real system this would be replaced by a persistent store.
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        code="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, 10mg daily"
    ),
    "P002": Patient(
        code="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}


# --------------------------------------------------------------------
# Helper utilities ---------------------------------------------------
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_PLACEHOLDER_PATTERN = re.compile(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}")

def _validate_template(template: str) -> None:
    """
    Ensure the template does not reference sensitive patient data.
    Raises ValueError if a sensitive field is used.
    """
    for match in _PLACEHOLDER_PATTERN.finditer(template):
        field = match.group(1)
        if field in _SENSITIVE_FIELDS:
            raise ValueError(
                f"Access to sensitive patient field '{field}' is not allowed."
            )


def _build_mapping(patient: Patient) -> Dict[str, str]:
    """
    Build a dictionary mapping placeholder names to their string values.
    Only non‑sensitive fields are exposed.
    """
    patient_dict = asdict(patient)
    # Exclude sensitive data
    for field in _SENSITIVE_FIELDS:
        patient_dict.pop(field, None)
    # Convert all values to string for formatting
    return {k: str(v) for k, v in patient_dict.items()}


# --------------------------------------------------------------------
# Public API ---------------------------------------------------------
def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient‑specific report from the given template.

    Parameters
    ----------
    patient_code : str
        The unique identifier of the patient.
    report_template : str
        A template string containing placeholders such as '{patient.name}'.

    Returns
    -------
    str
        The formatted report string with non‑sensitive patient data.

    Raises
    ------
    ValueError
        If the patient is not found or if the template attempts to access
        sensitive data.
    """
    # 1. Retrieve patient record safely
    patient = _PATIENT_DB.get(patient_code)
    if patient is None:
        raise ValueError(f"Patient with code '{patient_code}' not found.")

    # 2. Validate the template for sensitive fields
    _validate_template(report_template)

    # 3. Build a mapping of allowed fields
    mapping = _build_mapping(patient)

    # 4. Perform safe formatting
    try:
        formatted_report = report_template.format(patient=mapping)
    except KeyError as exc:
        # This means the template referenced a field that doesn't exist
        raise ValueError(f"Unknown placeholder in template: {exc}") from exc

    return formatted_report


# --------------------------------------------------------------------
# Example usage (uncomment to test)
# if __name__ == "__main__":
#     template = "Patient {patient.name} (Age: {patient.age}) is a {patient.gender}."
#     print(create_person_report("P001", template))