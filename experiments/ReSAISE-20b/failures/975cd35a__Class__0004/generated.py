import re
from dataclasses import dataclass, field
from typing import Dict

# --------------------------------------------------------------------------- #
#  Patient model and in‑memory repository (mocked for this example)
# --------------------------------------------------------------------------- #

@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str = field(repr=False)          # sensitive data
    treatment_plan: str = field(repr=False)     # sensitive data

# Mock database of patients
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# --------------------------------------------------------------------------- #
#  Report generation
# --------------------------------------------------------------------------- #

_RESTRICTED_FIELDS = {"diagnosis", "treatment_plan"}

_PLACEHOLDER_PATTERN = re.compile(r"\{([^}]+)\}")

def _get_patient(patient_id: str) -> Patient:
    """Retrieve a patient from the mock database."""
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")
    return patient

def _validate_template(template: str) -> None:
    """
    Ensure the template does not request restricted data.
    Raises ValueError if a forbidden placeholder is detected.
    """
    for match in _PLACEHOLDER_PATTERN.finditer(template):
        key = match.group(1).strip()
        # We expect keys in the form 'patient.<attribute>'
        if key.startswith("patient."):
            attr = key.split(".", 1)[1]
            if attr in _RESTRICTED_FIELDS:
                raise ValueError(f"Access to restricted field '{attr}' is not allowed.")
        else:
            # Any other placeholder format is considered invalid
            raise ValueError(f"Unsupported placeholder '{key}' in template.")

def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a report string by filling in placeholders with patient data.

    Parameters
    ----------
    patient_identifier : str
        Unique identifier of the patient.
    template_string : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string.

    Raises
    ------
    ValueError
        If the patient ID is invalid or if the template requests restricted data.
    """
    # Validate that the template doesn't expose sensitive info
    _validate_template(template_string)

    patient = _get_patient(patient_identifier)

    # Prepare a safe mapping of allowed attributes
    allowed_attrs = {
        f"patient.{field}": getattr(patient, field)
        for field in patient.__dataclass_fields__
        if field not in _RESTRICTED_FIELDS
    }

    try:
        report = template_string.format(**allowed_attrs)
    except KeyError as exc:
        # Placeholder refers to an attribute that does not exist
        raise ValueError(f"Unknown placeholder in template: {exc}") from None

    return report