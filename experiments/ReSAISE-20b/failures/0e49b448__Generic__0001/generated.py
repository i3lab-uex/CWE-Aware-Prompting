import re
from dataclasses import dataclass, asdict
from typing import Dict

# ------------------------------------------------------------------
# Patient model (non‑sensitive fields only)
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    # Sensitive fields are omitted from the public dataclass

# ------------------------------------------------------------------
# In‑memory patient store (for demo purposes)
# ------------------------------------------------------------------
PATIENT_STORE: Dict[str, Patient] = {
    "P001": Patient(patient_id="P001", name="Alice Smith", age=34, gender="F"),
    "P002": Patient(patient_id="P002", name="Bob Johnson", age=47, gender="M"),
    # ... add more patients as needed
}

# ------------------------------------------------------------------
# Helper: Detect if a template references a sensitive field
# ------------------------------------------------------------------
SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
PLACEHOLDER_PATTERN = re.compile(r"{\s*patient\.([a-zA-Z_][a-zA-Z0-9_]*)\s*}")

def _validate_template(template: str) -> None:
    """
    Raise ValueError if the template tries to access sensitive fields.
    """
    for match in PLACEHOLDER_PATTERN.finditer(template):
        field_name = match.group(1)
        if field_name in SENSITIVE_FIELDS:
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited")

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def build_patient_summary(patient_key: str, template_string: str) -> str:
    """
    Build a patient summary string from the given template.

    Parameters
    ----------
    patient_key : str
        The unique identifier of the patient.
    template_string : str
        A string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted patient summary string.

    Raises
    ------
    ValueError
        If the patient ID is not found or if the template contains a
        sensitive field.
    """
    # 1. Retrieve patient record
    patient = PATIENT_STORE.get(patient_key)
    if not patient:
        raise ValueError(f"Patient ID '{patient_key}' not found")

    # 2. Validate that the template does not reference sensitive fields
    _validate_template(template_string)

    # 3. Prepare a safe namespace for formatting
    patient_dict = asdict(patient)
    safe_namespace = {"patient": patient_dict}

    # 4. Perform formatting
    try:
        result = template_string.format(**safe_namespace)
    except KeyError as exc:
        # A placeholder referenced a field that doesn't exist
        raise ValueError(f"Unknown field in template: {exc}") from exc

    return result