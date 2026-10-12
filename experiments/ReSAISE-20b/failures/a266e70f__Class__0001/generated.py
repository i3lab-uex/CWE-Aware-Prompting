import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Sample data model and storage
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Represents a patient record."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str            # Sensitive data
    treatment_plan: str       # Sensitive data

# In‑memory patient store (for illustration only)
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Lisinopril 10mg daily"
    ),
    "p002": Patient(
        id="p002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Albuterol inhaler as needed"
    ),
}

# ----------------------------------------------------------------------
# Authorization & policy helpers
# ----------------------------------------------------------------------
def _is_authorized(patient_id: str) -> bool:
    """
    Dummy authorization check.
    In a real system this would query the authentication/authorization layer.
    """
    # For demonstration: only allow access to patients whose ID starts with 'p0'
    return patient_id in _PATIENT_DB

# ----------------------------------------------------------------------
# Report generation
# ----------------------------------------------------------------------
_PLACEHOLDER_PATTERN = re.compile(r"\{patient\.([a-zA-Z_]+)\}")

# Allowed non‑sensitive fields
_ALLOWED_FIELDS = {"name", "age", "gender"}

def create_patient_report(id: str, report_template: str) -> str:
    """
    Generates a patient report by filling placeholders in *report_template*
    with data from the patient record identified by *id*.

    Parameters
    ----------
    id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The report with all placeholders replaced by actual patient data.

    Raises
    ------
    ValueError
        If the patient ID is unknown, if access to the record is not authorized,
        or if the template attempts to expose restricted data.
    """
    # 1. Validate patient ID
    if not _is_authorized(id):
        raise ValueError(f"Unauthorized or unknown patient ID: {id}")

    patient = _PATIENT_DB[id]

    # 2. Find all placeholders in the template
    placeholders = _PLACEHOLDER_PATTERN.findall(report_template)

    # 3. Validate each placeholder
    for field in placeholders:
        if field not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Attempt to access restricted patient data: '{field}'. "
                "Only name, age, and gender are allowed in public reports."
            )

    # 4. Prepare substitution dictionary
    subs = {field: getattr(patient, field) for field in placeholders}

    # 5. Perform safe formatting
    try:
        report = report_template.format(patient=patient, **subs)
    except KeyError as exc:
        # This should not happen because we validated fields above
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report