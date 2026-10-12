import re
from dataclasses import dataclass

# ----------------------------------------------------
# Mock patient storage (in a real system this would be
# replaced with database access or an external service)
# ----------------------------------------------------
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    treatment_plan: str  # considered sensitive


# Example in‑memory patient registry
PATIENT_REGISTRY = {
    "p001": Patient(
        patient_id="p001",
        name="John Doe",
        age=45,
        gender="Male",
        diagnosis="Hypertension",
        treatment_plan="Medication A, Lifestyle changes"
    ),
    # Add more patients as needed
}


def _get_patient_by_id(patient_id: str) -> Patient:
    """Retrieve a patient from the registry or raise ValueError."""
    patient = PATIENT_REGISTRY.get(patient_id)
    if not patient:
        raise ValueError(f"Patient with ID '{patient_id}' not found.")
    return patient


# ----------------------------------------------------
# Report generation
# ----------------------------------------------------
_ALLOWED_FIELDS = {
    "name",
    "age",
    "gender",
    "diagnosis",  # Non‑sensitive field
    # Note: 'treatment_plan' is intentionally omitted to prevent accidental exposure
}


_PLACEHOLDER_RE = re.compile(r"\{patient\.([a-zA-Z_][a-zA-Z0-9_]*)\}")


def generate_user_report(patient_id: str, template: str) -> str:
    """
    Generate a report string for the given patient ID by substituting
    placeholders in the template with actual patient data.

    Parameters:
        patient_id (str): Identifier of the patient.
        template   (str): Report template containing placeholders like
                          '{patient.name}', '{patient.age}'.

    Returns:
        str: The rendered report string.

    Raises:
        ValueError: If the patient is not found, a placeholder refers to
                    an unauthorized or non‑existent attribute, or any other
                    error occurs during rendering.
    """
    try:
        patient = _get_patient_by_id(patient_id)

        def replace(match: re.Match) -> str:
            field = match.group(1)
            if field not in _ALLOWED_FIELDS:
                raise ValueError(f"Access to unauthorized or unknown field '{field}'.")
            value = getattr(patient, field)
            return str(value)

        rendered = _PLACEHOLDER_RE.sub(replace, template)
        return rendered

    except Exception as exc:
        # Any exception is treated as a security or data access issue
        raise ValueError(f"Failed to generate report: {exc}") from exc


# ----------------------------------------------------
# Example usage (uncomment for testing)
# ----------------------------------------------------
# if __name__ == "__main__":
#     tmpl = "Patient Report:\nName: {patient.name}\nAge: {patient.age}\nDiagnosis: {patient.diagnosis}"
#     print(generate_user_report("p001", tmpl))