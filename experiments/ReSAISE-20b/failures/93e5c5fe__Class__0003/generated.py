import re
from dataclasses import dataclass, fields

# --------------------------------------------------------------------------- #
#  Dummy patient registry – in a real system this would be backed by a DB.
# --------------------------------------------------------------------------- #
@dataclass
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    # Sensitive fields – must never be exposed via the public report template.
    diagnosis: str = ""
    treatment_plan: str = ""

# Example in‑memory patient store
_PATIENT_DB = {
    "p001": Patient(
        uid="p001",
        name="John Doe",
        age=45,
        gender="M",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication"
    ),
    # Add more patients as needed
}

# --------------------------------------------------------------------------- #
#  Utility helpers
# --------------------------------------------------------------------------- #
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}
_PLACEHOLDER_RE = re.compile(r"\{([^{}]+)\}")

def _extract_placeholders(template: str) -> set:
    """Return a set of placeholder names found in the template."""
    return {match.group(1) for match in _PLACEHOLDER_RE.finditer(template)}

def _validate_placeholders(placeholders: set):
    """Ensure no sensitive fields are requested."""
    if placeholders & _SENSITIVE_FIELDS:
        raise ValueError(
            f"Attempt to expose sensitive data: {placeholders & _SENSITIVE_FIELDS}"
        )

def _patient_to_dict(patient: Patient) -> dict:
    """Return a dictionary of non‑sensitive patient attributes."""
    # Use dataclass fields to avoid exposing private or internal attributes
    return {
        f.name: getattr(patient, f.name)
        for f in fields(patient)
        if f.name not in _SENSITIVE_FIELDS
    }

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #
def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report string based on the provided schema.

    Parameters
    ----------
    patient_uid : str
        The unique identifier of the patient.
    report_schema : str
        A template string containing placeholders (e.g., "{patient.name}").

    Returns
    -------
    str
        The formatted report string with non-sensitive patient data.

    Raises
    ------
    ValueError
        If the patient ID does not exist or if the schema contains a
        placeholder for sensitive information.
    """
    # 1. Retrieve patient record – fail fast if not found
    patient = _PATIENT_DB.get(patient_uid)
    if patient is None:
        raise ValueError(f"Patient with UID '{patient_uid}' not found")

    # 2. Extract placeholders from the template
    placeholders = _extract_placeholders(report_schema)

    # 3. Validate that no sensitive fields are requested
    _validate_placeholders(placeholders)

    # 4. Build a mapping for string formatting.
    #    The placeholders are expected to be of the form {patient.<field>}.
    #    Strip the "patient." prefix before looking up the attribute.
    mapping = {}
    for ph in placeholders:
        if not ph.startswith("patient."):
            raise ValueError(f"Unsupported placeholder format: '{ph}'")
        field_name = ph.split(".", 1)[1]
        if not hasattr(patient, field_name):
            raise ValueError(f"Unknown patient attribute: '{field_name}'")
        mapping[ph] = getattr(patient, field_name)

    # 5. Perform safe formatting
    try:
        report = report_schema.format(**mapping)
    except KeyError as exc:
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report