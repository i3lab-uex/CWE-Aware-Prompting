import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
# Domain model – Patient records (simplified for this example)
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Patient:
    """Represents a patient record. Only non‑sensitive data should be exposed."""
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive – must never be revealed
    treatment_plan: str     # Sensitive – must never be revealed

# --------------------------------------------------------------------------- #
# In‑memory patient repository
# --------------------------------------------------------------------------- #

# For demonstration purposes we keep a simple dict.
PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication A"
    ),
    "P002": Patient(
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Medication B, diet plan"
    ),
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

_ALLOWED_FIELDS = {"name", "age", "gender"}  # fields allowed in the template
_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Build a patient summary by applying ``template_string`` to the patient record
    identified by ``patient_key``.

    Parameters
    ----------
    patient_key : str
        The unique identifier for a patient.
    template_string : str
        A string containing placeholders of the form ``{patient.<field>}``.

    Returns
    -------
    str
        The rendered summary string.

    Raises
    ------
    ValueError
        If the patient key is unknown or if the template tries to access a
        sensitive field (diagnosis, treatment_plan).
    """
    # --------------------------------------------------------------------- #
    # 1. Retrieve patient record
    # --------------------------------------------------------------------- #
    patient = PATIENT_DB.get(patient_key)
    if patient is None:
        raise ValueError(f"Patient with key '{patient_key}' not found.")

    # --------------------------------------------------------------------- #
    # 2. Validate and replace placeholders
    # --------------------------------------------------------------------- #
    def _replace(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in _ALLOWED_FIELDS:
            raise ValueError(
                f"Attempted to expose sensitive field '{field_name}'. "
                "Only name, age, and gender are allowed."
            )
        value = getattr(patient, field_name)
        # Convert non-string values to string for safe rendering
        return str(value)

    try:
        rendered = _PLACEHOLDER_RE.sub(_replace, template_string)
    except re.error as exc:
        # This should not happen under normal circumstances
        raise ValueError(f"Invalid template: {exc}") from exc

    return rendered

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tmpl = "Patient {patient.name}, age {patient.age}, gender {patient.gender}."
    print(build_patient_summary("P001", tmpl))