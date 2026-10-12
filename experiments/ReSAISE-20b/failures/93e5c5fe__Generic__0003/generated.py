import re
from dataclasses import dataclass, field
from typing import Dict

# ------------------------------------------------------------------
# Patient model – only non‑sensitive fields are permitted in the report
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Patient:
    uid: str
    name: str
    age: int
    gender: str
    # Sensitive data – should never be exposed in a public report
    diagnosis: str = field(repr=False)
    treatment_plan: str = field(repr=False)

# ------------------------------------------------------------------
# In‑memory patient registry – replace with real DB lookup in production
# ------------------------------------------------------------------
_PATIENT_REGISTRY: Dict[str, Patient] = {
    "123": Patient(
        uid="123",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    "456": Patient(
        uid="456",
        name="Jane Smith",
        age=30,
        gender="Female",
        diagnosis="Diabetes",
        treatment_plan="Insulin therapy"
    ),
}

# ------------------------------------------------------------------
# Helper: find placeholders of the form {patient.<field>}
# ------------------------------------------------------------------
_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")

# ------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------
def compose_patient_report(patient_uid: str, report_schema: str) -> str:
    """
    Generate a patient report string by substituting placeholders in the
    provided schema with values from the patient's record.

    Args:
        patient_uid: Unique identifier of the patient.
        report_schema: Template string containing placeholders like
                       `{patient.name}`, `{patient.age}`.

    Returns:
        A fully rendered string with non-sensitive patient data.

    Raises:
        ValueError: If the patient does not exist, or if a sensitive field
                    (diagnosis, treatment_plan) is referenced in the schema.
    """
    # ------------------------------------------------------------------
    # 1. Retrieve patient
    # ------------------------------------------------------------------
    patient = _PATIENT_REGISTRY.get(patient_uid)
    if not patient:
        raise ValueError(f"Patient with UID '{patient_uid}' not found.")

    # ------------------------------------------------------------------
    # 2. Identify placeholders
    # ------------------------------------------------------------------
    placeholders = _PLACEHOLDER_RE.findall(report_schema)

    # If no placeholders, just return the schema as is
    if not placeholders:
        return report_schema

    # ------------------------------------------------------------------
    # 3. Validate and replace each placeholder
    # ------------------------------------------------------------------
    def _replace(match: re.Match) -> str:
        field_name = match.group(1)
        # Disallow sensitive fields
        if field_name in {"diagnosis", "treatment_plan"}:
            raise ValueError(f"Access to sensitive field '{field_name}' is prohibited.")
        # Ensure the attribute exists
        if not hasattr(patient, field_name):
            raise ValueError(f"Patient has no attribute '{field_name}'.")
        value = getattr(patient, field_name)
        return str(value)

    rendered_report = _PLACEHOLDER_RE.sub(_replace, report_schema)
    return rendered_report

# ------------------------------------------------------------------
# Example usage (uncomment to test)
# ------------------------------------------------------------------
# if __name__ == "__main__":
#     template = "Patient: {patient.name}, Age: {patient.age}, Gender: {patient.gender}"
#     print(compose_patient_report("123", template))