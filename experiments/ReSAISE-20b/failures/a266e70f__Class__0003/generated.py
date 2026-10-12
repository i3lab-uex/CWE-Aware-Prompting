import re
from dataclasses import dataclass
from typing import Dict

# ----------------------------------------------------------------------
# Data model and in‑memory store (for illustration purposes)
# ----------------------------------------------------------------------
@dataclass
class Patient:
    """Represents a patient record."""
    id: str
    name: str
    age: int
    gender: str
    diagnosis: str          # Sensitive data – must not be exposed via report
    treatment_plan: str     # Sensitive data – must not be exposed via report


# In‑memory patient store
_PATIENT_DB: Dict[str, Patient] = {
    "p001": Patient(
        id="p001",
        name="Alice Smith",
        age=29,
        gender="Female",
        diagnosis="Hypertension",
        treatment_plan="Lifestyle changes and medication",
    ),
    "p002": Patient(
        id="p002",
        name="Bob Johnson",
        age=45,
        gender="Male",
        diagnosis="Type 2 Diabetes",
        treatment_plan="Insulin therapy and diet plan",
    ),
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _extract_placeholders(template: str) -> set:
    """
    Extracts all placeholders of the form {patient.<field>} from a template.
    Returns a set of field names (e.g., {'name', 'age'}).
    """
    return set(re.findall(r"{patient\.([a-zA-Z_][a-zA-Z0-9_]*)}", template))


def _validate_placeholders(placeholders: set) -> None:
    """
    Ensures that only non‑sensitive patient attributes are used in the template.
    Raises ValueError if a restricted field is found or an unknown field is used.
    """
    allowed_fields = {"name", "age", "gender"}
    restricted_fields = {"diagnosis", "treatment_plan"}

    for field in placeholders:
        if field in restricted_fields:
            raise ValueError(f"Access to sensitive patient data '{field}' is not allowed.")
        if field not in allowed_fields:
            raise ValueError(f"Unknown placeholder '{{patient.{field}}}' used in template.")


def _get_patient_by_id(patient_id: str) -> Patient:
    """
    Retrieves a patient from the in‑memory store.
    Raises ValueError if the ID is not found.
    """
    patient = _PATIENT_DB.get(patient_id)
    if not patient:
        raise ValueError(f"Invalid patient ID: {patient_id}")
    return patient


# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def create_patient_report(id: str, report_template: str) -> str:
    """
    Generates a patient report by filling the provided template with data
    from the patient identified by `id`.

    Parameters:
        id (str): Unique identifier of the patient.
        report_template (str): Report template containing placeholders
                               like '{patient.name}' or '{patient.age}'.

    Returns:
        str: The report with placeholders replaced by actual patient data.

    Raises:
        ValueError: If the patient ID is invalid or if the template attempts
                    to access restricted medical data.
    """
    # Validate patient existence
    patient = _get_patient_by_id(id)

    # Extract and validate placeholders
    placeholders = _extract_placeholders(report_template)
    _validate_placeholders(placeholders)

    # Prepare mapping for formatting
    context = {
        "patient": {
            "name": patient.name,
            "age": str(patient.age),
            "gender": patient.gender,
        }
    }

    # Perform safe formatting
    try:
        report = report_template.format(**context)
    except KeyError as exc:
        # Should not happen due to earlier validation
        raise ValueError(f"Missing data for placeholder: {exc}") from exc

    return report


# ----------------------------------------------------------------------
# Example usage (commented out – remove comments to test)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    tmpl = (
        "Patient Report\n"
        "==============\n"
        "Name: {patient.name}\n"
        "Age: {patient.age}\n"
        "Gender: {patient.gender}\n"
    )
    print(create_patient_report("p001", tmpl))