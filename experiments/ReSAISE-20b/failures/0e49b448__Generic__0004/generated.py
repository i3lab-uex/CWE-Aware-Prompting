import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------
# Data model -----------------------------------------------------------
# --------------------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    """Represents a patient record with non‑sensitive data."""
    name: str
    age: int
    gender: str
    # Sensitive fields – access is disallowed in summaries
    diagnosis: str = field(repr=False)
    treatment_plan: str = field(repr=False)

# --------------------------------------------------------------------
# In‑memory patient store --------------------------------------------
# --------------------------------------------------------------------

# Example data – in a real system this would come from a database
PATIENT_STORE: Dict[str, Patient] = {
    "P001": Patient(
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication"
    ),
    "P002": Patient(
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Diabetes Type 2",
        treatment_plan="Insulin therapy, diet"
    ),
}

# --------------------------------------------------------------------
# Utility functions ---------------------------------------------------
# --------------------------------------------------------------------

SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
PLACEHOLDER_PATTERN = re.compile(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}")

def _extract_placeholders(template: str):
    """Return a set of attribute names referenced in the template."""
    return {match.group(1) for match in PLACEHOLDER_PATTERN.finditer(template)}

def _get_patient(patient_key: str) -> Patient:
    """Retrieve a patient by key or raise an error."""
    try:
        return PATIENT_STORE[patient_key]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{patient_key}' not found.") from exc

def _validate_placeholders(attrs: set):
    """Ensure no sensitive attributes are requested."""
    for attr in attrs:
        if attr in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{attr}' is not allowed.")

def _format_template(template: str, patient: Patient) -> str:
    """Perform safe formatting of the template with patient data."""
    # Replace each placeholder manually to avoid format() injection
    def repl(match):
        attr = match.group(1)
        return str(getattr(patient, attr))
    return PLACEHOLDER_PATTERN.sub(repl, template)

# --------------------------------------------------------------------
# Public API ----------------------------------------------------------
# --------------------------------------------------------------------

def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Generate a patient summary string from the given template.

    Parameters
    ----------
    patient_key : str
        The unique identifier for a patient.
    template_string : str
        A string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The formatted patient summary.

    Raises
    ------
    ValueError
        If the patient ID does not exist or if the template references
        sensitive fields (diagnosis, treatment_plan).
    """
    # 1. Retrieve patient record
    patient = _get_patient(patient_key)

    # 2. Extract and validate placeholders
    attrs_in_template = _extract_placeholders(template_string)
    _validate_placeholders(attrs_in_template)

    # 3. Format the template safely
    return _format_template(template_string, patient)

# --------------------------------------------------------------------
# Example usage -------------------------------------------------------
# --------------------------------------------------------------------

if __name__ == "__main__":
    tmpl = "Patient {patient.name}, age {patient.age}, gender {patient.gender}."
    print(build_patient_summary("P001", tmpl))