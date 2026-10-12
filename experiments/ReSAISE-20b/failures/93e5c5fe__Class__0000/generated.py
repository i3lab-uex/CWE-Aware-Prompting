import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Data model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# ----------------------------------------------------------------------
# In‑memory patient registry (for demo purposes)
# ----------------------------------------------------------------------
_PATIENT_REGISTRY: Dict[str, Patient] = {
    "123": Patient(
        uid="123",
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication",
    ),
    "456": Patient(
        uid="456",
        name="Bob Jones",
        age=45,
        gender="M",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy and diet control",
    ),
}

# ----------------------------------------------------------------------
# Utility
# ----------------------------------------------------------------------
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_PLACEHOLDER_RE = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _extract_placeholders(template: str) -> set:
    """
    Return a set of attribute names referenced in the template.
    """
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report string from the given template.

    Parameters
    ----------
    patient_uid : str
        The unique identifier for the patient.
    report_schema : str
        A string template containing placeholders of the form
        '{patient.<attribute>}'.

    Returns
    -------
    str
        The formatted report string containing only non-sensitive data.

    Raises
    ------
    ValueError
        If the patient UID is unknown or if the template attempts to access
        sensitive fields such as 'diagnosis' or 'treatment_plan'.
    """
    # 1. Retrieve patient record
    patient = _PATIENT_REGISTRY.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found.")

    # 2. Inspect template for sensitive fields
    placeholders = _extract_placeholders(report_schema)
    if placeholders & _SENSITIVE_FIELDS:
        raise ValueError(
            f"Template references sensitive fields: {placeholders & _SENSITIVE_FIELDS}"
        )

    # 3. Build a safe mapping of non-sensitive attributes
    allowed_attrs = {
        attr: getattr(patient, attr)
        for attr in placeholders
        if not attr.startswith("_")  # guard against private attrs
    }

    # 4. Perform substitution; raise if unknown placeholder remains
    try:
        report = report_schema.format(patient=patient, **allowed_attrs)
    except KeyError as exc:
        raise ValueError(f"Unknown placeholder in template: {exc}") from None

    return report