import re
from dataclasses import dataclass, asdict
from typing import Dict

# ----------------------------------------------------
# Data model
# ----------------------------------------------------
@dataclass(frozen=True)
class Patient:
    """Represents a patient in the system."""
    identifier: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive

# ----------------------------------------------------
# In‑memory patient store (simulating a database)
# ----------------------------------------------------
_PATIENT_DB: Dict[str, Patient] = {
    "patient-001": Patient(
        identifier="patient-001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "patient-002": Patient(
        identifier="patient-002",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Asthma",
        treatment_plan="Inhaler B, Avoid triggers"
    ),
}

# ----------------------------------------------------
# Report builder
# ----------------------------------------------------
def build_patient_report(patient_identifier: str, template_string: str) -> str:
    """
    Build a patient report by substituting placeholders in the template with
    data from the specified patient.

    Placeholders are of the form `{patient.<field>}`.  Only a limited set
    of non‑sensitive fields are allowed to be exposed in reports.

    Args:
        patient_identifier: The unique identifier of the patient.
        template_string: The template string containing placeholders.

    Returns:
        A fully rendered report string.

    Raises:
        ValueError: If the patient ID is unknown, or if a placeholder
                    references an unsupported or restricted field.
    """
    # --------------------------------------------------------
    # 1. Retrieve patient data
    # --------------------------------------------------------
    patient = _PATIENT_DB.get(patient_identifier)
    if not patient:
        raise ValueError(f"Patient ID '{patient_identifier}' is invalid.")

    # --------------------------------------------------------
    # 2. Prepare safe mapping
    # --------------------------------------------------------
    # Only expose non‑sensitive attributes.
    allowed_fields = {"name", "age", "gender"}
    patient_dict = {k: v for k, v in asdict(patient).items() if k in allowed_fields}

    # --------------------------------------------------------
    # 3. Replace placeholders safely
    # --------------------------------------------------------
    placeholder_pattern = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

    def _replace(match: re.Match) -> str:
        field_name = match.group(1)
        if field_name not in allowed_fields:
            raise ValueError(f"Access to restricted or unknown patient field '{field_name}'.")
        value = patient_dict[field_name]
        return str(value)

    try:
        report = placeholder_pattern.sub(_replace, template_string)
    except re.error as exc:  # pragma: no cover
        raise ValueError(f"Template string error: {exc}") from exc

    return report


# ----------------------------------------------------
# Example usage (commented out)
# ----------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Patient: {patient.name}, Age: {patient.age}, Gender: {patient.gender}"
#     print(build_patient_report("patient-001", tmpl))