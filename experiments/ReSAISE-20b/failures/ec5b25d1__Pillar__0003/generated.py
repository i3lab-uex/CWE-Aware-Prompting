import re
from dataclasses import dataclass, fields
from typing import Dict

# --------------------------------------------------------------------------- #
#  Patient data model and a simple in‑memory registry for demo purposes
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Non‑sensitive patient record."""
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# Example registry – in a real system this would be replaced by a database lookup
PATIENT_REGISTRY: Dict[str, Patient] = {
    "P001": Patient(
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        name="Jane Smith",
        age=32,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------------- #
#  Helper functions
# --------------------------------------------------------------------------- #

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of patient attribute names referenced in the template."""
    return set(_PLACEHOLDER_RE.findall(template))

def _validate_placeholders(placeholders: set) -> None:
    """Ensure that no sensitive fields are requested."""
    if placeholders & _SENSITIVE_FIELDS:
        raise ValueError(
            f"Attempt to access sensitive patient information: {placeholders & _SENSITIVE_FIELDS}"
        )

def _patient_to_dict(patient: Patient) -> dict:
    """Return a mapping of patient attributes for formatting."""
    return {f.name: getattr(patient, f.name) for f in fields(patient)}

# --------------------------------------------------------------------------- #
#  Main function
# --------------------------------------------------------------------------- #

def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient report string from the provided template.

    Parameters
    ----------
    patient_code : str
        The unique identifier for a patient.
    report_template : str
        A template string containing placeholders such as `{patient.name}`.

    Returns
    -------
    str
        The formatted report string containing only non‑sensitive data.

    Raises
    ------
    ValueError
        If the patient ID is unknown or if the template attempts to access
        sensitive fields such as `diagnosis` or `treatment_plan`.
    """
    # 1. Retrieve patient record
    patient = PATIENT_REGISTRY.get(patient_code)
    if not patient:
        raise ValueError(f"Patient ID '{patient_code}' not found.")

    # 2. Parse placeholders and validate
    placeholders = _extract_placeholders(report_template)
    if not placeholders:
        # No placeholders – return the template unchanged
        return report_template

    _validate_placeholders(placeholders)

    # 3. Prepare substitution dictionary
    patient_dict = _patient_to_dict(patient)
    subs = {f"patient.{k}": v for k, v in patient_dict.items() if k not in _SENSITIVE_FIELDS}

    # 4. Perform safe formatting
    try:
        formatted = report_template.format(**subs)
    except KeyError as exc:
        missing_field = str(exc).strip("'")
        raise ValueError(f"Missing patient attribute in template: {missing_field}") from None

    return formatted