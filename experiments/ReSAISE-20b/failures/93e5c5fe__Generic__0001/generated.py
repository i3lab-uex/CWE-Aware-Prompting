import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Domain model ---------------------------------------------------------
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    diagnosis: str          # sensitive
    treatment_plan: str     # sensitive


# --------------------------------------------------------------------
# In‑memory patient repository ---------------------------------------
# --------------------------------------------------------------------

# For demonstration purposes we use a simple dictionary as a
# stand‑in for a database. In production this would be replaced by
# an ORM or a dedicated data‑access layer.
_PATIENT_DB: Dict[str, Patient] = {}

def add_patient(patient: Patient) -> None:
    """Utility helper to populate the in‑memory store."""
    _PATIENT_DB[patient.uid] = patient


# --------------------------------------------------------------------
# Report composition --------------------------------------------------
# --------------------------------------------------------------------

# Allowed non‑sensitive fields that can be used in the template.
_ALLOWED_FIELDS = {"name", "age", "gender"}

# Sensitive fields that must not appear in the report.
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}


def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report by substituting placeholders in *report_schema*
    with data from the patient identified by *patient_uid*.

    Parameters
    ----------
    patient_uid : str
        Unique identifier of the patient.
    report_schema : str
        Template string containing placeholders like ``{patient.name}``.

    Returns
    -------
    str
        The rendered report.

    Raises
    ------
    ValueError
        If the patient UID is unknown, or if a sensitive field is referenced.
    """
    # ----------------------------------------------------------------
    # 1. Retrieve patient ------------------------------------------------
    # ----------------------------------------------------------------
    patient = _PATIENT_DB.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found.")

    # ----------------------------------------------------------------
    # 2. Find all placeholders in the template -------------------------
    # ----------------------------------------------------------------
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")
    placeholders = placeholder_pattern.findall(report_schema)

    # ----------------------------------------------------------------
    # 3. Validate placeholders -----------------------------------------
    # ----------------------------------------------------------------
    for field_name in set(placeholders):
        if field_name in _SENSITIVE_FIELDS:
            raise ValueError(
                f"Attempt to access sensitive patient data: '{field_name}'."
            )
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Unknown patient field '{field_name}' in report template."
            )

    # ----------------------------------------------------------------
    # 4. Substitute placeholders ---------------------------------------
    # ----------------------------------------------------------------
    def replace_match(match: re.Match) -> str:
        field = match.group(1)
        return str(getattr(patient, field))

    rendered_report = placeholder_pattern.sub(replace_match, report_schema)
    return rendered_report


# --------------------------------------------------------------------
# Example usage --------------------------------------------------------
# --------------------------------------------------------------------
if __name__ == "__main__":
    # Populate the mock database
    add_patient(
        Patient(
            uid="12345",
            name="John Doe",
            age=42,
            gender="Male",
            diagnosis="Hypertension",
            treatment_plan="Medication A, Diet B",
        )
    )

    # Define a report template
    template = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )

    # Compose the report
    print(compose_patient_report("12345", template))