import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock data store – in a real system this would be a database or external API
# --------------------------------------------------------------------------- #
@dataclass
class Patient:
    identifier: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # sensitive data
    treatment_plan: str = field(repr=False)     # sensitive data

# In‑memory patient registry (identifier → Patient)
_PATIENT_REGISTRY: Dict[str, Patient] = {
    "123": Patient(
        identifier="123",
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication"
    ),
    "456": Patient(
        identifier="456",
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #
def _get_patient(identifier: str) -> Patient:
    """
    Retrieve a patient by identifier. Raises ValueError if not found.
    """
    try:
        return _PATIENT_REGISTRY[identifier]
    except KeyError as exc:
        raise ValueError(f"Patient ID '{identifier}' is invalid.") from exc

# --------------------------------------------------------------------------- #
# Main API
# --------------------------------------------------------------------------- #
def build_patient_summary(identifier: str, report_template: str) -> str:
    """
    Build a patient‑specific report by substituting placeholders in the
    provided template with data from the corresponding Patient object.

    Parameters
    ----------
    identifier : str
        Unique patient ID.
    report_template : str
        Template string containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The fully rendered report.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if restricted fields are requested.
    """
    # 1. Validate and fetch patient
    patient = _get_patient(identifier)

    # 2. Define allowed attributes (public information only)
    ALLOWED_ATTRS = {"name", "age", "gender"}

    # 3. Find all placeholders in the template
    placeholder_pattern = re.compile(r"\{([^{}]+)\}")
    placeholders = placeholder_pattern.findall(report_template)

    # 4. Prepare substitution dictionary
    subs: Dict[str, str] = {}
    for key in placeholders:
        # Expect keys of the form 'patient.<attr>'
        if not key.startswith("patient."):
            raise ValueError(f"Unsupported placeholder '{key}'.")
        attr = key.split(".", 1)[1]
        if attr not in ALLOWED_ATTRS:
            raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
        # Retrieve attribute value
        try:
            value = getattr(patient, attr)
        except AttributeError as exc:
            raise ValueError(f"Patient has no attribute '{attr}'.") from exc
        subs[key] = str(value)

    # 5. Perform substitution safely
    try:
        rendered = report_template.format(**subs)
    except KeyError as exc:
        raise ValueError(f"Missing substitution for placeholder {exc}") from exc

    return rendered