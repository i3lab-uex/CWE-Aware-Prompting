import re
from dataclasses import dataclass, field
from typing import Dict

# ----------------------------------------------------------------------
# Patient model
# ----------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    # Restricted data – should never be exposed in public reports
    diagnosis: str = field(repr=False)
    treatment_plan: str = field(repr=False)

# ----------------------------------------------------------------------
# In‑memory patient store (simulating a database)
# ----------------------------------------------------------------------
_PATIENT_STORE: Dict[str, Patient] = {
    "P001": Patient(
        patient_id="P001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, 5mg daily"
    ),
    "P002": Patient(
        patient_id="P002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, 2 puffs twice daily"
    ),
}

# ----------------------------------------------------------------------
# Helper: allowed placeholder keys
# ----------------------------------------------------------------------
_ALLOWED_KEYS = {"patient.name", "patient.age", "patient.gender"}

# Regular expression to find all placeholders in the template
_PLACEHOLDER_RE = re.compile(r"{([^}]+)}")

def _extract_placeholders(template: str) -> set:
    """Return a set of unique placeholders found in the template."""
    return {match.group(1).strip() for match in _PLACEHOLDER_RE.finditer(template)}

def generate_patient_summary(patient_id: str, report_template: str) -> str:
    """
    Generate a patient summary by replacing placeholders in the template
    with actual patient data.

    Parameters:
        patient_id (str): Unique identifier of the patient.
        report_template (str): Template string containing placeholders.

    Returns:
        str: The template with placeholders replaced by patient data.

    Raises:
        ValueError: If the patient_id is invalid, or if restricted data
                    is requested in the template.
    """
    # ------------------------------------------------------------------
    # 1. Validate patient existence
    # ------------------------------------------------------------------
    patient = _PATIENT_STORE.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")

    # ------------------------------------------------------------------
    # 2. Validate placeholders
    # ------------------------------------------------------------------
    placeholders = _extract_placeholders(report_template)
    for ph in placeholders:
        if ph not in _ALLOWED_KEYS:
            raise ValueError(
                f"Restricted or unknown placeholder '{ph}' in template."
            )

    # ------------------------------------------------------------------
    # 3. Prepare mapping for safe formatting
    # ------------------------------------------------------------------
    placeholder_map = {
        "patient.name": patient.name,
        "patient.age": str(patient.age),
        "patient.gender": patient.gender,
    }

    # ------------------------------------------------------------------
    # 4. Perform formatting
    # ------------------------------------------------------------------
    try:
        result = report_template.format(**placeholder_map)
    except KeyError as exc:  # pragma: no cover
        # Should not happen due to prior validation, but guard anyway
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return result