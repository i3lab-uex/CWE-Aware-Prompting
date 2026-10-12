import re
from dataclasses import dataclass, asdict
from typing import Dict

# ---------- Patient model ----------
@dataclass(frozen=True)
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # restricted data
    treatment_plan: str     # restricted data

# ---------- In‑memory patient store ----------
_PATIENT_DB: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="Alice Smith",
        age=34,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes, medication",
    ),
    "P002": Patient(
        patient_id="P002",
        name="Bob Johnson",
        age=58,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy, diet control",
    ),
}

# ---------- Allowed fields for report ----------
_ALLOWED_FIELDS = {"name", "age", "gender"}

# ---------- Utility ----------
def _extract_placeholders(template: str) -> set:
    """Return a set of field names referenced as {patient.<field>}."""
    pattern = r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}"
    return set(re.findall(pattern, template))

# ---------- Main function ----------
def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Replace placeholders in `report_template` with data from the patient
    identified by `patient_id`.

    Parameters
    ----------
    patient_id : str
        Unique identifier of the patient.
    report_template : str
        Template string containing placeholders like `{patient.name}`.

    Returns
    -------
    str
        The template with placeholders substituted by patient data.

    Raises
    ------
    ValueError
        If the patient_id is not found or if a restricted field is requested.
    """
    # 1. Validate patient existence
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")

    # 2. Parse placeholders
    placeholders = _extract_placeholders(report_template)

    # 3. Check for restricted fields
    if not placeholders <= _ALLOWED_FIELDS:
        forbidden = placeholders - _ALLOWED_FIELDS
        raise ValueError(
            f"Attempt to access restricted patient data: {', '.join(forbidden)}"
        )

    # 4. Prepare mapping for str.format
    patient_dict = asdict(patient)
    format_map = {f"patient.{k}": v for k, v in patient_dict.items() if k in _ALLOWED_FIELDS}

    # 5. Perform substitution
    try:
        result = report_template.format(**format_map)
    except KeyError as e:
        # This should not happen due to prior checks, but guard anyway
        raise ValueError(f"Missing data for placeholder: {e}") from e

    return result