import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
#   Patient data model (non‑sensitive fields only)
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    # Sensitive fields are omitted from the public API
    _diagnosis: str | None = None          # marked private, not exposed
    _treatment_plan: str | None = None     # marked private, not exposed


# --------------------------------------------------------------------------- #
#   In‑memory patient repository (for demo purposes)
# --------------------------------------------------------------------------- #

_patient_repository: Dict[str, Patient] = {}


def register_patient(patient: Patient) -> None:
    """Add a patient to the repository."""
    _patient_repository[patient.uid] = patient


# --------------------------------------------------------------------------- #
#   Report composition
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}


def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report string by applying ``report_schema`` to the
    patient's non‑sensitive data.

    Parameters
    ----------
    patient_uid : str
        Unique identifier of the patient.
    report_schema : str
        Template containing placeholders like ``{patient.name}`` or
        ``{patient.age}``.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient is not found or if the template references a
        sensitive field.
    """
    # 1. Resolve patient record
    patient = _patient_repository.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found.")

    # 2. Parse template for placeholders
    placeholder_pattern = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")
    placeholders = placeholder_pattern.findall(report_schema)

    # 3. Validate fields
    for field_name in placeholders:
        if field_name in _SENSITIVE_FIELDS:
            raise ValueError(
                f"Attempted to access sensitive field '{field_name}'. "
                "Only non‑sensitive data is allowed."
            )
        # Ensure field exists on Patient
        if not any(f.name == field_name for f in fields(patient)):
            raise ValueError(
                f"Field '{field_name}' is not a valid attribute of Patient."
            )

    # 4. Build context dictionary for formatting
    context = {f"patient.{name}": getattr(patient, name) for name in placeholders}

    # 5. Format the report
    try:
        report = report_schema.format(**context)
    except KeyError as exc:  # pragma: no cover
        raise ValueError(f"Missing data for placeholder {exc}") from exc

    return report


# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Register a patient
    p = Patient(
        uid="12345",
        name="John Doe",
        age=30,
        gender="Male",
        _diagnosis="Hypertension",
        _treatment_plan="Lifestyle changes and medication"
    )
    register_patient(p)

    # Define a report template
    schema = (
        "Patient Report:\n"
        "Name: {patient.name}\n"
        "Age: {patient.age} years\n"
        "Gender: {patient.gender}\n"
    )

    # Compose report
    print(compose_patient_report("12345", schema))