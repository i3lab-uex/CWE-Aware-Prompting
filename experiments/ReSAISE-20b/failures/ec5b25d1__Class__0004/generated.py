import re
from dataclasses import dataclass
from typing import Dict

# --------------------------------------------------------------------------- #
#  Patient model (simplified)
# --------------------------------------------------------------------------- #
@dataclass
class Patient:
    """Represents a patient record with non‑sensitive and sensitive fields."""
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive
    treatment_plan: str     # Sensitive


# --------------------------------------------------------------------------- #
#  In‑memory patient repository (for demo purposes)
# --------------------------------------------------------------------------- #
_PATIENTS: Dict[str, Patient] = {
    "P001": Patient(
        name="Alice Smith",
        age=29,
        gender="F",
        diagnosis="Hypertension",
        treatment_plan="Medication A, 10mg daily"
    ),
    "P002": Patient(
        name="Bob Johnson",
        age=45,
        gender="M",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy, diet plan"
    ),
}

# --------------------------------------------------------------------------- #
#  Helper utilities
# --------------------------------------------------------------------------- #
_SENSITIVE_FIELDS = {"diagnosis", "treatment_plan"}


def _extract_placeholders(template: str) -> set:
    """
    Extract all placeholders in the form {patient.<field>} from a template string.
    Returns a set of field names.
    """
    pattern = r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}"
    return set(re.findall(pattern, template))


def _get_patient(patient_code: str) -> Patient:
    """
    Retrieve a patient by code. Raises ValueError if not found.
    """
    patient = _PATIENTS.get(patient_code)
    if patient is None:
        raise ValueError(f"Patient with code '{patient_code}' not found.")
    return patient


def _prepare_context(patient: Patient) -> Dict[str, str]:
    """
    Build a mapping for the template. Only non‑sensitive fields are exposed.
    """
    context = {
        "name": patient.name,
        "age": str(patient.age),
        "gender": patient.gender,
    }
    return context


# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #
def create_person_report(patient_code: str, report_template: str) -> str:
    """
    Generate a patient‑specific report from a template.

    Parameters
    ----------
    patient_code : str
        Unique identifier for the patient.
    report_template : str
        Template containing placeholders like '{patient.name}'.

    Returns
    -------
    str
        The formatted report string with non‑sensitive patient data.

    Raises
    ------
    ValueError
        If the patient is not found or if the template references sensitive data.
    """
    # Validate input
    if not isinstance(patient_code, str) or not patient_code.strip():
        raise ValueError("patient_code must be a non‑empty string.")
    if not isinstance(report_template, str):
        raise ValueError("report_template must be a string.")

    # Retrieve patient record
    patient = _get_patient(patient_code)

    # Detect attempts to access sensitive fields
    placeholders = _extract_placeholders(report_template)
    if placeholders & _SENSITIVE_FIELDS:
        raise ValueError(
            f"Template attempts to expose sensitive fields: {sorted(placeholders & _SENSITIVE_FIELDS)}"
        )

    # Build context and format
    context = _prepare_context(patient)
    try:
        report = report_template.format(patient=context)
    except KeyError as exc:
        # In case the template references an unknown field
        raise ValueError(f"Unknown placeholder in template: {exc}") from None

    return report


# --------------------------------------------------------------------------- #
#  Example usage (commented out – remove to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    tmpl = "Patient {patient.name} ({patient.age}) is a {patient.gender}."
    print(create_person_report("P001", tmpl))