import re
from dataclasses import dataclass

# ----------------------------------------------------------------------
# Domain model – Patient
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Immutable patient record."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str

# ----------------------------------------------------------------------
# In‑memory data store (replace with real DB in production)
# ----------------------------------------------------------------------
_PATIENT_DB = {
    "P001": Patient(
        id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ----------------------------------------------------------------------
# Allowed attributes for substitution
# ----------------------------------------------------------------------
_ALLOWED_ATTRS = {
    "name",
    "age",
    "gender",
    "diagnosis",
    "treatment_plan"
}

# ----------------------------------------------------------------------
# Helper – safe placeholder extraction
# ----------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str):
    """Return a set of placeholder names found in the template."""
    return set(match.group(1) for match in _PLACEHOLDER_RE.finditer(template))

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report for the given patient by replacing placeholders in
    `template` with actual patient data.

    Parameters
    ----------
    patient_id : str
        The identifier of the patient to report on.
    template : str
        A string containing placeholders such as `{patient.name}`.

    Returns
    -------
    str
        The report with all placeholders substituted.

    Raises
    ------
    ValueError
        If the patient does not exist, a placeholder refers to an invalid
        attribute, or if the template contains disallowed content.
    """
    # --------------------------------------------------------------
    # 1. Retrieve patient record (simulated lookup)
    # --------------------------------------------------------------
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID '{patient_id}' not found.")

    # --------------------------------------------------------------
    # 2. Validate placeholders
    # --------------------------------------------------------------
    placeholders = _extract_placeholders(template)

    for field in placeholders:
        if field not in _ALLOWED_ATTRS:
            raise ValueError(f"Unauthorized placeholder '{{patient.{field}}}' detected.")
        # Ensure the attribute actually exists on Patient
        if not hasattr(patient, field):
            raise ValueError(f"Patient object missing attribute '{field}'.")

    # --------------------------------------------------------------
    # 3. Perform substitution
    # --------------------------------------------------------------
    def _replacement(match):
        field_name = match.group(1)
        return str(getattr(patient, field_name))

    try:
        report = _PLACEHOLDER_RE.sub(_replacement, template)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Failed to generate report: {exc}") from exc

    return report