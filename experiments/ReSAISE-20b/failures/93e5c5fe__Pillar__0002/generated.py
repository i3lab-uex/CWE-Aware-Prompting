import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Patient data model – only non‑sensitive fields are exposed for formatting
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    # Sensitive fields – not exposed via the public interface
    _diagnosis: str = field(repr=False, compare=False)
    _treatment_plan: str = field(repr=False, compare=False)

    @property
    def diagnosis(self):
        raise AttributeError("Access to sensitive field 'diagnosis' is prohibited")

    @property
    def treatment_plan(self):
        raise AttributeError("Access to sensitive field 'treatment_plan' is prohibited")

# --------------------------------------------------------------------------- #
# In‑memory patient registry (for demo purposes – replace with DB lookup)
# --------------------------------------------------------------------------- #
_PATIENT_REGISTRY: Dict[str, Patient] = {
    "uid-001": Patient(
        uid="uid-001",
        name="Alice Smith",
        age=29,
        gender="Female",
        _diagnosis="Hypertension",
        _treatment_plan="Lifestyle changes, medication A"
    ),
    "uid-002": Patient(
        uid="uid-002",
        name="Bob Jones",
        age=45,
        gender="Male",
        _diagnosis="Diabetes Type II",
        _treatment_plan="Insulin therapy, diet"
    ),
}

# --------------------------------------------------------------------------- #
# Helper to parse template placeholders
# --------------------------------------------------------------------------- #
_placeholder_pattern = re.compile(r"{([^{}]+)}")

def _extract_placeholders(template: str):
    """Return a set of unique placeholder names found in the template."""
    return {match.group(1).strip() for match in _placeholder_pattern.finditer(template)}

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #
def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report based on the provided schema.

    Parameters
    ----------
    patient_uid : str
        Unique identifier of the patient.
    report_schema : str
        Template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        Formatted report string with non‑sensitive patient data.

    Raises
    ------
    ValueError
        If the patient UID is not found or if the template tries to access
        sensitive fields (diagnosis, treatment_plan).
    """
    # Retrieve patient record
    patient = _PATIENT_REGISTRY.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found")

    # Validate placeholders – disallow sensitive fields
    for placeholder in _extract_placeholders(report_schema):
        # Expect format 'patient.<field>'
        if not placeholder.startswith("patient."):
            raise ValueError(f"Invalid placeholder '{placeholder}'. Must start with 'patient.'")
        field_name = placeholder.split(".", 1)[1]
        if field_name in {"diagnosis", "treatment_plan"}:
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited")

    # Prepare a mapping for safe formatting
    context = {
        "patient.name": patient.name,
        "patient.age": patient.age,
        "patient.gender": patient.gender,
    }

    # Perform formatting
    try:
        formatted = report_schema.format(**context)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from None

    return formatted