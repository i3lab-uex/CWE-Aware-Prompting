import re
from dataclasses import dataclass, fields
from typing import Dict

# --- Domain model ---------------------------------------------------------

@dataclass(frozen=True)
class Patient:
    name: str
    age: int
    gender: str
    diagnosis: str          # sensitive
    treatment_plan: str     # sensitive

# --- In‑memory patient repository -----------------------------------------

# Example data – in a real system this would come from a database
PATIENTS: Dict[str, Patient] = {
    "P001": Patient(
        name="Alice Smith",
        age=34,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        name="Bob Johnson",
        age=58,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy, Diet plan"
    ),
}

# --- Helper utilities -----------------------------------------------------

_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def _extract_placeholders(template: str):
    """Return a set of patient attribute names used in the template."""
    return {m.group(1) for m in _PLACEHOLDER_RE.finditer(template)}

def _replace_placeholders(patient: Patient, template: str) -> str:
    """Safely replace placeholders with patient data."""
    def repl(match):
        field = match.group(1)
        if field in _SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive patient data '{field}' is not allowed.")
        # getattr will raise AttributeError if the field does not exist
        return str(getattr(patient, field))
    return _PLACEHOLDER_RE.sub(repl, template)

# --- Public API -----------------------------------------------------------

def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Build a patient summary string based on the provided template.

    Parameters
    ----------
    patient_key : str
        Identifier for the patient.
    template_string : str
        Template containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The formatted patient summary.

    Raises
    ------
    ValueError
        If the patient is not found or a sensitive field is requested.
    """
    if patient_key not in PATIENTS:
        raise ValueError(f"Patient with key '{patient_key}' not found.")

    patient = PATIENTS[patient_key]

    # Check for sensitive fields before performing replacement
    placeholders = _extract_placeholders(template_string)
    if any(field in _SENSITIVE_FIELDS for field in placeholders):
        raise ValueError("Template contains references to sensitive patient data.")

    # Perform the replacement
    try:
        result = _replace_placeholders(patient, template_string)
    except AttributeError as exc:
        # If the placeholder refers to a non‑existent field
        raise ValueError(f"Invalid template: {exc}") from exc

    return result

# --- Example usage (uncomment to test) ------------------------------------
# if __name__ == "__main__":
#     tmpl = "Patient {patient.name}, age {patient.age}, gender {patient.gender}."
#     print(build_patient_summary("P001", tmpl))